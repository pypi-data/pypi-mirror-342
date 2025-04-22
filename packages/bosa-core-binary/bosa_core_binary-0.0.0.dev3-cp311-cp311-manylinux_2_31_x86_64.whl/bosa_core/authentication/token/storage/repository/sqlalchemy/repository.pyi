from _typeshed import Incomplete
from bosa_core.authentication.database import DatabaseAdapter as DatabaseAdapter
from bosa_core.authentication.token.storage.models import Token as Token
from bosa_core.authentication.token.storage.repository.base_repository import BaseTokenRepository as BaseTokenRepository
from bosa_core.authentication.token.storage.repository.sqlalchemy.models import DBToken as DBToken
from sqlalchemy.engine import Engine as Engine
from uuid import UUID

class SqlAlchemyTokenRepository(BaseTokenRepository):
    """SQLAlchemy token repository."""
    db: Incomplete
    def __init__(self, engine_or_url: Engine | str, pool_size: int = 50, max_overflow: int = 0, autoflush: bool = True) -> None:
        """Initialize the repository.

        Args:
            engine_or_url (Engine|str): The database engine or URL.
            pool_size (int): The size of the database connections to be maintained. Default is 50.
            max_overflow (int): The maximum overflow size of the pool. Default is 0.
            autoflush (bool): If True, all changes to the database are flushed immediately. Default is True.

        Raises:
            ValueError: If the database adapter is not initialized.
        """
    def get_token(self, client_id: UUID, user_id: UUID, token_id: UUID) -> Token | None:
        """Get token.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.
            token_id (UUID): Token ID.

        Returns:
            Token: The token
        """
    def create_token(self, token: Token) -> None:
        """Create token.

        Args:
            token (Token): The token
        """
    def revoke_token(self, client_id: UUID, user_id: UUID, token_id: UUID) -> bool:
        """Revoke a token.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.
            token_id (UUID): Token ID.

        Returns:
            bool: True if token was found and revoked, False otherwise
        """
