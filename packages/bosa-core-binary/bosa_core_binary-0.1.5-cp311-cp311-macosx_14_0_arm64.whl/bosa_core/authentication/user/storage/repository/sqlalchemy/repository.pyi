from _typeshed import Incomplete
from bosa_core.authentication.database import DatabaseAdapter as DatabaseAdapter
from bosa_core.authentication.token.service.create_token_service import CreateTokenService as CreateTokenService
from bosa_core.authentication.token.storage.repository.sqlalchemy.repository import SqlAlchemyTokenRepository as SqlAlchemyTokenRepository
from bosa_core.authentication.token.storage.token_storage import TokenStorage as TokenStorage
from bosa_core.authentication.user.storage.models import UserModel as UserModel
from bosa_core.authentication.user.storage.repository.base_repository import BaseRepository as BaseRepository
from bosa_core.authentication.user.storage.repository.sqlalchemy.models import DBUser as DBUser
from sqlalchemy.engine import Engine as Engine
from uuid import UUID

class SqlAlchemyUserRepository(BaseRepository):
    """User repository."""
    token_service: Incomplete
    db: Incomplete
    def __init__(self, engine_or_url: Engine | str, pool_size: int = 50, max_overflow: int = 0, autoflush: bool = True) -> None:
        """Initialize the repository.

        Args:
            engine_or_url (Engine|str): The database engine or URL.
            pool_size (int): The size of the database connections to be maintained. Default is 50.
            max_overflow (int): The maximum overflow size of the pool. Default is 0.
            autoflush (bool): If True, all changes to the database are flushed immediately. Default is True.
        """
    def get_user(self, client_id: UUID, user_id: UUID) -> UserModel | None:
        """Retrieves a user.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.

        Returns:
            UserModel: User object.
        """
    def get_user_by_identifier(self, client_id: UUID, identifier: str) -> UserModel | None:
        """Retrieves a user.

        Args:
            client_id (UUID): Client ID.
            identifier (str): User identifier.

        Returns:
            UserModel | None: User object or None if not found.
        """
    def create_user(self, user: UserModel) -> UserModel:
        """Creates a new user.

        Args:
            user (UserModel): User model.

        Returns:
            UserModel: Created user.
        """
