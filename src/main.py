from datetime import datetime
import logging
import time
import os, sys

from ping3 import ping

import psycopg2
from psycopg2 import OperationalError
from psycopg2.sql import SQL, Identifier, Placeholder

import logger

class Database:
    dbconnection = None

    @classmethod
    def create_connection(cls):
        try:
            connection = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST", "db"),
                port=5432
            )
            logging.info(f'Connection to PostgreSQL successful')
            cls.connection = connection
        except Exception as e:
            logging.error(f'Error connecting to PostgreSQL: {e}')

    @classmethod
    def create_table(cls):
        connection = cls.dbconnection
        if connection:
            try:
                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS ping_status (
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP UNIQUE,
                                id INT,
                                ping_value NUMERIC(5,2),
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
                        ''')
                        logging.info("Table 'ping_status' checked/created successfully")
            except OperationalError as e:
                logging.error(f"Error creating table: {e}")
            # finally:
            #     connection.close()

    @classmethod
    def insert_ping_status(cls, timestamp, id, ping_value):
        connection = cls.dbconnection
        if connection:
            try:
                with connection:
                    with connection.cursor() as cursor:
                        cursor.execute('''
                            INSERT INTO ping_status (timestamp, id, ping_value)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (timestamp) DO UPDATE 
                            SET ping_value = EXCLUDED.ping_value;
                        ''', (timestamp, id, ping_value))
                        print("Ping status inserted/updated successfully")
            except OperationalError as e:
                print(f"Error inserting ping status: {e}")
            # finally:
            #     connection.close()

    @classmethod
    def close_connection(cls):
        cls.dbconnection.close()

class Metrics:
    ID = 0

    @classmethod
    def get_current_time(cls):
        return datetime.now()

    @classmethod
    def custom_ping(cls, host):
        ret = {'time': None, 'id': None, 'ping': None}

        # Main task of the function
        ping_ms = ping(host, unit='ms')

        # If ping is fine, insert it into dict, otherwise insert Null
        # In Grafana we want to see if something has been dropped
        if ping_ms:
            ret['ping'] = round(ping_ms, 2)
        else:
            ret['ping'] = None
            logging.error(f"Request timed out for {host}")

        ret['time'] = cls.get_current_time()
        ret['id'] = cls.ID

        cls.ID += 1
        logging.info(f"{ret['time'].strftime("%Y-%m-%d_%H-%M-%S")}, {ret['id']}, {ret['ping']}")

        return ret.values()



if __name__ == '__main__':
    try:
        Database.create_connection()
        Database.create_table()
    
        while True:
            timestamp, id, ping_value = Metrics.custom_ping('8.8.8.8')
            Database.insert_ping_status(timestamp=timestamp, id=id, ping_value=ping_value)
            time.sleep(1)
    except Exception as e:
        logging.error(f'Metrics app runnig  error - {e}')
    finally:
        Database.close_connection()