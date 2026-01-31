from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

def config(return_url=False):
    db = {
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT', 5432),
        'database': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
    }

    if return_url:
        db = f'postgresql://{db['user']}:{db['password']}@{db["host"]}:{db["port"]}/{db["database"]}'

    return db