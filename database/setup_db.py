import os
import psycopg2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load database credentials from environment variables
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/tradingbot")


def setup_database():
    """Creates the database tables from the migration SQL file."""
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()

        # Read migrations.sql and execute the queries
        with open("database/migrations.sql", "r") as file:
            sql_script = file.read()
            cursor.execute(sql_script)

        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Database setup completed successfully.")

    except Exception as e:
        logger.error(f"Database setup failed: {e}")


if __name__ == "__main__":
    setup_database()
