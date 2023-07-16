"""
Django command to wait for the database to be available
"""
import time

from typing import Any
from django.db.utils import OperationalError
from psycopg import OperationalError as Psycopg3Error
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """django command to wait for db"""

    def handle(self, *args: Any, **options: Any) -> str | None:
        """entrypoint for command"""
        self.stdout.write("Waiting for database")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg3Error, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second ...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Dabase available"))
