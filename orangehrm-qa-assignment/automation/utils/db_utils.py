import psycopg2
import logging
from typing import Dict, List, Optional, Union
from pathlib import Path
from config.settings import settings
from contextlib import contextmanager
import pandas as pd

logger = logging.getLogger(__name__)

class DatabaseUtils:
    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        """Establish database connection with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.connection = psycopg2.connect(
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    database=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    connect_timeout=5
                )
                logger.info("Database connection established")
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Database connection failed after {max_retries} attempts: {str(e)}")
                    raise
                logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")

    @contextmanager
    def get_cursor(self):
        """Provide transactional scope with automatic commit/rollback"""
        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Transaction failed: {str(e)}")
            raise
        finally:
            cursor.close()

    def execute_query(self, query: str, params: Optional[tuple] = None, return_df: bool = False) -> Union[List[Dict], pd.DataFrame]:
        """Execute query with optional DataFrame return"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    return pd.DataFrame(data) if return_df else data
                return pd.DataFrame() if return_df else []
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise

    def execute_script(self, script_path: Path):
        """Execute SQL script with transaction handling"""
        try:
            with open(script_path) as f:
                sql = f.read()
            with self.get_cursor() as cursor:
                cursor.execute(sql)
            logger.info(f"Executed SQL script: {script_path}")
        except Exception as e:
            logger.error(f"Script execution failed: {str(e)}")
            raise

    def table_to_df(self, table_name: str, where: str = "") -> pd.DataFrame:
        """Convert database table to DataFrame"""
        query = f"SELECT * FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        return self.execute_query(query, return_df=True)

    def close(self):
        """Close connection with cleanup"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            logger.info("Database connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
