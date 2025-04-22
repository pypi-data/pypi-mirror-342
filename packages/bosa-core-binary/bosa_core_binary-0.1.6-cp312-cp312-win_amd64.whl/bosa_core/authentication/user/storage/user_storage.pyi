from _typeshed import Incomplete
from bosa_core.authentication.user.storage.models import UserModel as UserModel
from bosa_core.authentication.user.storage.repository.base_repository import BaseRepository as BaseRepository
from uuid import UUID

class UserStorage:
    """User storage."""
    repository: Incomplete
    def __init__(self, repository: BaseRepository) -> None:
        """Initialize the storage.

        Args:
            repository (BaseRepository): The repository
        """
    def get_user(self, client_id: UUID, user_id: UUID) -> UserModel | None:
        """Get user.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.

        Returns:
            UserModel | None: The user model or None
        """
    def get_user_by_identifier(self, client_id: UUID, identifier: str) -> UserModel:
        """Get user by identifier.

        Args:
            client_id (UUID): Client ID.
            identifier (str): User identifier.

        Returns:
            UserModel: The user model
        """
    def create_user(self, user: UserModel) -> UserModel:
        """Creates a new user.

        Args:
            user (UserModel): User model.

        Returns:
            UserModel: Created user.
        """
