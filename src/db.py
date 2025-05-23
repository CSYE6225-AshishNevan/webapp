from sqlmodel import SQLModel, create_engine, Session, select, text

import logging
from datetime import datetime, timezone

from src.models.User import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CONN_STRING = "postgresql://ashishnevan:postgresql@localhost:5432/mydb"


def connect():
    """
    Connect to the database.
    """
    # Create a new SQLAlchemy engine instance
    engine = create_engine(CONN_STRING)
    return engine


def test_connection(engine=connect()) -> bool:
    """
    Test the database connection.
    """
    res = False
    with Session(engine) as session:
        try:
            # Execute a simple query to test the connection
            result = session.exec(text("SELECT 1"))
            if result.scalar() == 1:
                logger.info("Database connection successful.")
                res = True
            else:
                logger.error("Database connection failed.")
        except Exception as e:
            logger.error(f"Error testing database connection: {e}")
    return res


def bootstrap() -> bool:
    """
    Bootstrap the database.
    """
    # Create a new SQLAlchemy engine instance
    res = _create_tables(connect())
    if res:
        logger.info("Database bootstrapped successfully.")
    else:
        logger.error("Failed to bootstrap the database.")
    return res


def create_user(new_user: User) -> bool:
    """
    Create a new user in the database.
    """
    engine = connect()
    res = False
    try:
        with Session(engine) as session:
            session.add(new_user)
            session.commit()
        res = True
        logger.info("User created successfully.")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
    return res


def get_user_from_email(email: str) -> User | None:
    """
    Get a user from the database by email.
    """
    engine = connect()
    res = None
    with Session(engine) as session:
        try:
            # Query the user by email
            user = session.exec(select(User).where(User.email == email)).first()
            if user is not None:
                res = user
                logger.info(f"User found: {res}")
            else:
                logger.info("User not found.")
        except Exception as e:
            logger.error(f"Error getting user from email: {e}")
    return res


def update_user_with_id(user_id: int, user: User) -> bool:
    """
    Update a user in the database by ID.
    """
    engine = connect()
    res = False
    with Session(engine) as session:
        try:
            existing_user = session.exec(select(User).where(User.id == user_id)).first()
            if existing_user is not None:
                existing_user.first_name = user.first_name
                existing_user.last_name = user.last_name
                existing_user.password = user.password
                existing_user.account_updated = datetime.now(timezone.utc)
                session.commit()
                res = True
                logger.info(f"User updated successfully: {existing_user}")
            else:
                logger.info("User not found.")
        except Exception as e:
            logger.error(f"Error updating user: {e}")
    return res


def _create_tables(conn):
    """
    Create tables in the database.
    """
    res = False
    try:
        SQLModel.metadata.create_all(bind=conn)
        res = True
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
    return res
