from datetime import datetime
import logging
import time
import os, sys

from ping3 import ping

import psycopg2
from psycopg2.sql import SQL, Identifier, Placeholder

import logger

pg_host = os.getenv("DB_HOST", "localhost")
pg_database = os.getenv("DB_NAME", "postgres")
pg_user = os.getenv("DB_USER", "postgres")
pg_password = os.getenv("DB_PASSWORD", "postgres")

class Database:
    def create_pg_connection():
        """Create and return a PostgreSQL connection."""
        logging.info("Creating PostgreSQL connection")
        return psycopg.connect(
            f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}"
        )


class Metrics:
    ID = 0

    @classmethod
    def get_current_time(cls):
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


    @classmethod
    def custom_ping(cls, host):
        ret = {
            'time': None,
            'ID':   None,
            'ping': None
        }

        ping_ms = ping(host, unit='ms')

        if ping_ms:
            ret['time'] = cls.get_current_time()
            ret['ID'] = cls.ID
            ret['ping'] = round(ping_ms, 2)
            
            cls.ID += 1

            logging.info(ret)
            # print(f"Reply from {host}: Time={rtt:.2f}ms")
        else:
            ret = 1
            logging.error(f"Request timed out for {host}")

        return ret

# TODO: ping can be actually env variable
while True:
    Metrics.custom_ping('8.8.8.8')
    time.sleep(1)
# Ping has to run every x amount of time and store the result in database
