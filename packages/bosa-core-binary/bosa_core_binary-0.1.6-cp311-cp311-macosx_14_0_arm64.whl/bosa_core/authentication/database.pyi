from _typeshed import Incomplete
from bosa_core.authentication.config import AuthenticationDbSettings as AuthenticationDbSettings
from bosa_core.authentication.database_migration.migration import run_migrations as run_migrations
from bosa_core.exception.base import UninitializedException as UninitializedException
from collections.abc import Generator
from sqlalchemy.engine import Engine as Engine
from sqlalchemy.orm import sessionmaker

engine: Engine
session: sessionmaker
base: Incomplete

def initialize_authentication_db(settings: AuthenticationDbSettings):
    """Initialize the database engine and session.

    Args:
        settings (AuthenticationDbSettings): Authentication database settings.
    """
def get_db() -> Generator[Incomplete]:
    """Get a database session.

    Returns:
        Session: Database session.
    """

class DatabaseAdapter:
    """Initializes a database engine and session using SQLAlchemy.

    Provides a scoped session and a base query property for interacting with the database.
    """
    engine: Incomplete
    db: Incomplete
    base: Incomplete
    @classmethod
    def initialize(cls, engine_or_url: Engine | str, pool_size: int = 50, max_overflow: int = 0, autocommit: bool = False, autoflush: bool = True):
        """Creates a new database engine and session.

        Must provide either an engine or a database URL.

        Args:
            engine_or_url (Engine|str): Sqlalchemy engine object or database URL.
            pool_size (int): The size of the database connections to be maintained. Default is 50.
            max_overflow (int): The maximum overflow size of the pool. Default is 0.
            autocommit (bool): If True, all changes to the database are committed immediately. Default is False.
            autoflush (bool): If True, all changes to the database are flushed immediately. Default is True.
        """
    @classmethod
    def has_table(cls, table_name: str):
        """Check if a table exists in the database.

        Args:
            table_name (str): Table name to check.

        Returns:
            bool: True if table exists in the database.
        """
