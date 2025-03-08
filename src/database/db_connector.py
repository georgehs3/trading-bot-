import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Missing DATABASE_URL in .env file!")

engine = create_engine(DATABASE_URL)


class DatabaseConnector:
    def __init__(self):
        self.engine = engine

    def get_connection(self):
        """Get database connection"""
        return self.engine.connect()


