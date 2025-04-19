import argparse
import contextlib
import logging
import os
import pathlib
import sys
import time
from ipaddress import (
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network,
    ip_address,
    ip_network,
)

import jinja2
import prometheus_client

from . import metrics
from .as_helper import load_cidr_blocks
from .data import NetFlowElasticsearch
from .exabgp_conf import load_neighbors
from .smtp import Mailer
from .state import DB

# Egress needed so far:
# - SMTP to relay
# - Internet, but only for the init-container route information fetcher

logger = logging.getLogger(__name__)

DB_FILE = pathlib.Path(os.environ.get("DDAM_DB_FILE", "ddam.db"))
NEIGHBORS_CONFIG_FILE = pathlib.Path(
    os.environ.get("DDAM_NEIGHBORS_CONFIG_FILE", "neighbors.json")
)
CIDR_BLOCKS_FILE = pathlib.Path(
    os.environ.get("DDAM_CIDR_BLOCKS_FILE", "cidr-blocks.json")
)

SAMPLING_FACTOR = int(os.environ.get("DDAM_SAMPLING_FACTOR", "10000"))
ES_ADDRESS = os.environ.get("DDAM_ES_ADDRESS", "http://localhost:9200")
EXCLUDES = (
    os.environ["DDAM_EXCLUDES"].split(",") if "DDAM_EXCLUDES" in os.environ else []
)
DDOS_THRESHOLD_MBPS = int(os.environ.get("DDAM_DDOS_THRESHOLD_MBPS", "2000"))
INTERVAL_MINUTES = int(os.environ.get("DDAM_INTERVAL_MINUTES", "5"))
MAX_EXPIRATION_HOURS = int(os.environ.get("DDAM_MAX_EXPIRATION_HOURS", "24"))
EMAIL_ENABLE = int(os.environ.get("DDAM_EMAIL_ENABLE", "0"))
EMAIL_FROM = os.environ.get("DDAM_EMAIL_FROM", "ddam")
EMAIL_RECIPIENTS = (
    os.environ["DDAM_EMAIL_RECIPIENTS"].split(",")
    if "DDAM_EMAIL_RECIPIENTS" in os.environ
    else []
)
SMTP_RELAY_ADDRESS = os.environ.get("DDAM_SMTP_RELAY_ADDRESS", "127.0.0.1")
SMTP_PORT = int(os.environ.get("DDAM_SMTP_PORT", "25"))
SMTP_SSL = int(os.environ.get("DDAM_SMTP_SSL", "0")) > 0
EXPORTER_PORT = int(os.environ.get("DDAM_EXPORTER_PORT", "9998"))

BLACKHOLE_EMAIL_TEMPLATE_FILE = (
    pathlib.Path(os.environ["DDAM_BLACKHOLE_EMAIL_TEMPLATE_FILE"])
    if "DDAM_BLACKHOLE_EMAIL_TEMPLATE_FILE" in os.environ
    else None
)

UNBLACKHOLE_EMAIL_TEMPLATE_FILE = (
    pathlib.Path(os.environ["DDAM_UNBLACKHOLE_EMAIL_TEMPLATE_FILE"])
    if "DDAM_UNBLACKHOLE_EMAIL_TEMPLATE_FILE" in os.environ
    else None
)


class Ddam:
    def __init__(
        self,
        db: DB,
        es: NetFlowElasticsearch,
        networks: set[IPv4Network | IPv6Network],
        neighbors: dict,
        ddos_threshold_mbps: int,
        interval_minutes: int,
        excludes: set[IPv4Network | IPv6Network | IPv4Address | IPv6Address]
        | None = None,
        mailer: Mailer | None = None,
        blackhole_email_template: str | None = None,
        unblackhole_email_template: str | None = None,
    ):
        self.db = db
        self.es = es
        self.networks = networks
        self.neighbors = neighbors
        self.ddos_threshold_mbps = ddos_threshold_mbps
        self.interval_minutes = interval_minutes
        self.excludes = excludes
        self.mailer = mailer

        jinja_env = jinja2.Environment(
            loader=jinja2.PackageLoader("ddam"), autoescape=False
        )

        if blackhole_email_template is not None:
            self.blackhole_email_template = jinja_env.from_string(
                blackhole_email_template
            )
        else:
            self.blackhole_email_template = jinja_env.get_template(
                "blackhole_email.txt.j2"
            )

        if unblackhole_email_template is not None:
            self.unblackhole_email_template = jinja_env.from_string(
                unblackhole_email_template
            )
        else:
            self.unblackhole_email_template = jinja_env.get_template(
                "unblackhole_email.txt.j2"
            )

    def ip_is_excluded(self, ip: IPv4Address | IPv6Address) -> bool:
        if self.excludes is None:
            return False

        if ip.version == 4:
            for exclude in self.excludes:
                if (type(exclude) is IPv4Network and ip in exclude) or (
                    type(exclude) is IPv4Address and ip == exclude
                ):
                    return True

        elif ip.version == 6:
            for exclude in self.excludes:
                if (type(exclude) is IPv6Network and ip in exclude) or (
                    type(exclude) is IPv6Address and ip == exclude
                ):
                    return True

        return False

    def ip_is_valid(self, ip: IPv4Address | IPv6Address) -> bool:
        if self.ip_is_excluded(ip):
            return False

        return any(ip in network for network in self.networks)

    def announce(self, ip: IPv4Address | IPv6Address) -> None:
        for neighbor_ip, neighbor_config in self.neighbors.items():
            if neighbor_ip.version == ip.version:
                communities_str = " ".join(neighbor_config["communities"])
                sys.stdout.write(
                    f"neighbor {neighbor_ip} announce route {ip}/{ip.max_prefixlen} "
                    f"next-hop self community [{communities_str}]\n"
                )
        sys.stdout.flush()

    def withdraw(self, ip: IPv4Address | IPv6Address) -> None:
        for neighbor_ip, neighbor_config in self.neighbors.items():
            if neighbor_ip.version == ip.version:
                communities_str = " ".join(neighbor_config["communities"])
                sys.stdout.write(
                    f"neighbor {neighbor_ip} withdraw route {ip}/{ip.max_prefixlen} "
                    f"next-hop self community [{communities_str}]\n"
                )
        sys.stdout.flush()

    def reannounce_active(self) -> None:
        for record in self.db.get_active():
            if self.ip_is_valid(record["ip"]):
                # Silently reannounce the active IP.
                self.announce(record["ip"])

            else:
                # If the IP is no longer valid - unblackhole it.
                self.unblackhole(record["ip"])

    def send_notifications(self, subject: str, body: str) -> None:
        if self.mailer is not None:
            try:
                self.mailer.send(
                    subject,
                    body,
                )
            except Exception as e:
                logger.warning("Failed to send email: %s", e)
                metrics.MAILER_FAILURES.inc()

    def blackhole(self, ip: IPv4Address | IPv6Address, bitrate_mbps: float) -> None:
        logger.debug("Blackholing %s", ip)
        self.announce(ip)
        record = self.db.add(ip)
        logger.info(
            "Blackholed %s until %s. Current rate is %smbps",
            ip,
            record["expiration"],
            int(bitrate_mbps),
        )

        metrics.BLACKHOLED_ADDRESSES.labels(version=ip.version).inc()
        metrics.TRAFFIC_RATE.labels(version=ip.version).observe(bitrate_mbps)

        self.send_notifications(
            f"Blackhole {ip}",
            self.blackhole_email_template.render(
                ip=ip,
                expiration=record["expiration"],
                bitrate_mbps=int(bitrate_mbps),
            ),
        )

    def unblackhole(self, ip: IPv4Address | IPv6Address) -> None:
        logger.debug("Unblackholing %s", ip)

        self.withdraw(ip)

        self.db.deactivate(ip)

        logger.info("Unblackholed %s", ip)

        metrics.UNBLACKHOLED_ADDRESSES.labels(version=ip.version).inc()

        self.send_notifications(
            f"Unblackhole {ip}", self.unblackhole_email_template.render(ip=ip)
        )

    def check(self) -> None:
        logger.debug("Checking")

        for record in self.db.get_expired():
            self.unblackhole(record["ip"])

        self.db.prune()

        top10 = self.es.get_top_by_network_bytes(
            10,
            excludes=self.excludes,
            range_minutes=self.interval_minutes,
        )
        for item in top10:
            if (
                self.ip_is_valid(item["ip"])
                and item["bitrate_mbps"] > self.ddos_threshold_mbps
            ):
                self.blackhole(item["ip"], item["bitrate_mbps"])

        active_records = list(self.db.get_active())

        metrics.ACTIVE_RECORDS.set(len(active_records))

        if active_records:
            max_counter = max(active_records, key=lambda x: x["counter"])["counter"]
        else:
            max_counter = 0

        metrics.MAX_RECURRING_ATTACKS.set(max_counter)


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()

    parser.add_argument("command", choices=("migrate", "run"))

    args = parser.parse_args()

    db = DB(DB_FILE, max_hours=MAX_EXPIRATION_HOURS)

    if args.command == "migrate":
        db.migrate()
    elif args.command == "run":
        prometheus_client.start_http_server(EXPORTER_PORT)

        es = NetFlowElasticsearch(ES_ADDRESS, SAMPLING_FACTOR)

        if EMAIL_ENABLE:
            mailer = Mailer(
                SMTP_RELAY_ADDRESS,
                SMTP_PORT,
                SMTP_SSL,
                email_from=EMAIL_FROM,
                recipients=EMAIL_RECIPIENTS,
            )

            if BLACKHOLE_EMAIL_TEMPLATE_FILE is not None:
                with open(BLACKHOLE_EMAIL_TEMPLATE_FILE) as f:
                    blackhole_email_template = f.read()
            else:
                blackhole_email_template = None
            if UNBLACKHOLE_EMAIL_TEMPLATE_FILE is not None:
                with open(UNBLACKHOLE_EMAIL_TEMPLATE_FILE) as f:
                    unblackhole_email_template = f.read()
            else:
                unblackhole_email_template = None
        else:
            mailer = None
            blackhole_email_template = None
            unblackhole_email_template = None

        networks = load_cidr_blocks(CIDR_BLOCKS_FILE)

        neighbors = load_neighbors(NEIGHBORS_CONFIG_FILE)

        excludes = set()

        for neighbor_ip, neighbor_config in neighbors.items():
            excludes.add(neighbor_ip)
            excludes.add(neighbor_config["local-address"])

        for e in EXCLUDES:
            with contextlib.suppress(ValueError):
                excludes.add(ip_address(e))
                excludes.add(ip_network(e))

        ddam = Ddam(
            db,
            es,
            networks,
            neighbors,
            ddos_threshold_mbps=DDOS_THRESHOLD_MBPS,
            interval_minutes=INTERVAL_MINUTES,
            excludes=excludes,
            mailer=mailer,
            blackhole_email_template=blackhole_email_template,
            unblackhole_email_template=unblackhole_email_template,
        )

        ddam.reannounce_active()

        while True:
            ddam.check()
            time.sleep(INTERVAL_MINUTES * 60)
