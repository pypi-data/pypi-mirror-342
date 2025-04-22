from _typeshed import Incomplete
from bosa_core.authentication.config import AuthenticationDbSettings as AuthenticationDbSettings
from bosa_core.authentication.token.storage.models import Token as Token, TokenComplete as TokenComplete
from bosa_core.authentication.token.storage.token_storage import TokenStorage as TokenStorage
from bosa_core.authentication.user.storage.models import User as User

class CreateTokenService:
    """Create Token Service."""
    token_storage: Incomplete
    def __init__(self, token_storage: TokenStorage) -> None:
        """Initialize the service.

        Args:
            token_storage (TokenStorage): The token storage
        """
    def create_token(self, user: User) -> TokenComplete:
        """Create token.

        Args:
            user: The user

        Returns:
            TokenComplete: The token complete
        """
