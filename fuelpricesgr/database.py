"""Contains the functionality needed to communicate with the database
"""
import contextlib
import datetime
import decimal
import logging
import sqlite3

from . import enums, settings

# The module logger
logger = logging.getLogger(__name__)


class Database:
    """The interface to the database.
    """
    DB_FILE = settings.DATA_PATH / 'db.sqlite'

    def __init__(self):
        """Create the database connection.
        """
        if not self.DB_FILE.exists():
            logger.info("Database does not exist, creating")
            self._create_db()
        self.conn = None

    def _create_db(self):
        """Create the database.
        """
        with sqlite3.connect(self.DB_FILE) as conn, contextlib.closing(conn.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE daily_country (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    fuel_type TEXT NOT NULL,
                    number_of_stations INTEGER,
                    price DECIMAL(4, 3),
                    UNIQUE(date, fuel_type)
                )
            """)

    def close(self):
        """Closes the connection to the database.
        """
        self.conn.close()

    def __enter__(self):
        self.conn = sqlite3.connect(self.DB_FILE)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def insert_daily_country_data(
            self, date: datetime.date, fuel_type: enums.FuelType, number_of_stations: int = None,
            price: decimal.Decimal = None):
        """Insert daily country data to the database.

        :param date: The date for the data.
        :param fuel_type: The fuel type.
        :param number_of_stations: The number of stations.
        :param price: The price.
        """
        with contextlib.closing(self.conn.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO daily_country(date, fuel_type, number_of_stations, price)
                VALUES(:date, :fuel_type, :number_of_stations, :price)
                ON CONFLICT(date, fuel_type) DO UPDATE SET number_of_stations = :number_of_stations, price = :price
            """, {
                'date': date, 'fuel_type': fuel_type.name, 'number_of_stations': number_of_stations, 'price': str(price)
            })

    def save(self):
        self.conn.commit()
