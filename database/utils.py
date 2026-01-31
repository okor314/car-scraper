import psycopg2
import time

from database.config import config


DATABASE_CONFIG = config()

def get_db(retries=5, delay=5):
    for attempt in range(retries):
        try:
            return psycopg2.connect(
                **DATABASE_CONFIG,
                connect_timeout=15
            )
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
