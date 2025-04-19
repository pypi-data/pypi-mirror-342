import datetime
import sqlite3
from collections.abc import Generator
from ipaddress import IPv4Address, IPv6Address, ip_address


class DB:
    def __init__(self, db_file: str, max_hours: int = 24):
        self._conn = sqlite3.connect(db_file, autocommit=False)
        self.max_hours = max_hours

    def __del__(self):
        if hasattr(self, "_conn"):
            self._conn.close()

    def migrate(self):
        sql = """CREATE TABLE IF NOT EXISTS targets (
ip TEXT PRIMARY KEY,
updated INTEGER,
active INTEGER,
counter INTEGER)"""
        with self._conn:
            self._conn.execute(sql)

    def add(self, ip: IPv4Address | IPv6Address) -> dict:
        """
        Add an IP.
        If the IP is already present - set it to active and
        increment the counter
        """

        sql = """INSERT INTO targets(ip, updated, active, counter)
VALUES (:ip, unixepoch(), 1, 0)
ON CONFLICT(ip) DO UPDATE
SET updated=unixepoch(), active=1, counter=counter+1
RETURNING ip, updated, counter, min(unixepoch() + (pow(2, counter) * 60 * 60), unixepoch() + :max_hours * 60 * 60)"""  # noqa: E501
        with self._conn:
            c = self._conn.execute(sql, {"ip": str(ip), "max_hours": self.max_hours})
            ip, updated, counter, expiration = c.fetchone()
            return {
                "ip": ip_address(ip),
                "updated": datetime.datetime.fromtimestamp(
                    updated, datetime.timezone.utc
                ),
                "counter": counter,
                "expiration": datetime.datetime.fromtimestamp(
                    expiration, datetime.timezone.utc
                ),
            }

    def get_expired(self) -> Generator[dict, None, None]:
        """
        Return expired records.
        Record expiration is progressive depending on the counter,
        so the first time it expires in 1 hour, then 2, 4, 8, and
        so on.
        Maximum expiration time is capped by max_hours which is
        one day by default.
        """

        sql = """SELECT ip, updated, counter FROM targets
WHERE active=1
AND updated < max(unixepoch() - (pow(2, counter) * 60 * 60), unixepoch() - :max_hours * 60 * 60)"""  # noqa: E501
        with self._conn:
            for row in self._conn.execute(sql, {"max_hours": self.max_hours}):
                ip, updated, counter = row
                yield {
                    "ip": ip_address(ip),
                    "updated": datetime.datetime.fromtimestamp(
                        updated, datetime.timezone.utc
                    ),
                    "counter": counter,
                }

    def deactivate(self, ip: IPv4Address | IPv6Address) -> None:
        with self._conn:
            self._conn.execute(
                "UPDATE targets SET active=0, updated=unixepoch() WHERE ip=:ip",
                {"ip": str(ip)},
            )

    def get_active(self) -> Generator[dict, None, None]:
        sql = """SELECT ip, updated, counter FROM targets
WHERE active=1
AND updated >= min(unixepoch() - (pow(2, counter) * 60 * 60), unixepoch() - :max_hours * 60 * 60)"""  # noqa: E501
        with self._conn:
            for row in self._conn.execute(sql, {"max_hours": self.max_hours}):
                ip, updated, counter = row
                yield {
                    "ip": ip_address(ip),
                    "updated": datetime.datetime.fromtimestamp(
                        updated, datetime.timezone.utc
                    ),
                    "counter": counter,
                }

    def prune(self) -> None:
        """
        Delete all inactive records older than max_hours
        """

        sql = """DELETE FROM targets
WHERE active=0
AND (updated < unixepoch() - (:max_hours * 60 * 60))"""

        with self._conn:
            self._conn.execute(sql, {"max_hours": self.max_hours})
