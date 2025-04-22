from _typeshed import Incomplete
from bosa_core.authentication.token.storage.models import Token as Token
from bosa_core.authentication.token.storage.repository.base_repository import BaseTokenRepository as BaseTokenRepository
from uuid import UUID

class TokenStorage:
    """Token storage."""
    repository: Incomplete
    def __init__(self, repository: BaseTokenRepository) -> None:
        """Initialize the storage with the given repository.

        Args:
            repository (BaseTokenRepository): The repository
        """
    def get_token(self, client_id: UUID, user_id: UUID, token_id: UUID) -> Token:
        """Get token.

        Args:
            client_id: The client ID
            user_id: The user ID
            token_id: The token ID (jti)

        Returns:
            Token: The token
        """
    def create_token(self, token: Token) -> None:
        """Create token.

        Args:
            token: The token
        """
    def revoke_token(self, client_id: UUID, user_id: UUID, token_id: UUID) -> bool:
        """Revoke a token.

        Args:
            client_id (UUID): The client ID
            user_id (UUID): The user ID
            token_id (UUID): The token ID (jti)

        Returns:
            bool: True if token was found and revoked, False otherwise
        """
