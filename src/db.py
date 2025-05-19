import sqlalchemy
from sqlalchemy import create_engine

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CONN_STRING = "postgresql://ashishnevan:postgresql@localhost:5432/mydb"


def connect() -> sqlalchemy.engine.base.Connection:
    """
    Connect to the database.
    """
    # Create a new SQLAlchemy engine instance
    try:
        engine = create_engine(CONN_STRING)
        connection = engine.connect()
        return connection
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return None
