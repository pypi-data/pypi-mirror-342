from _typeshed import Incomplete
from bosa_core.authentication.client.service.client_aware_service import ClientAwareService as ClientAwareService
from bosa_core.authentication.client.service.verify_client_service import VerifyClientService as VerifyClientService
from bosa_core.authentication.client.storage.client_storage import ClientStorage as ClientStorage
from bosa_core.authentication.config import AuthenticationDbSettings as AuthenticationDbSettings
from bosa_core.authentication.user.helper.helper import UserHelper as UserHelper
from bosa_core.authentication.user.storage.models import UserModel as UserModel
from bosa_core.authentication.user.storage.user_storage import UserStorage as UserStorage
from bosa_core.exception.base import UserAlreadyExistsException as UserAlreadyExistsException

class CreateUserService(ClientAwareService):
    """Create user service."""
    USER_SECRET_PREVIEW_LENGTH: int
    user_storage: Incomplete
    verify_client_service: Incomplete
    user_helper: Incomplete
    hash_service: Incomplete
    def __init__(self, user_storage: UserStorage, client_storage: ClientStorage) -> None:
        """Initialize the service.

        Args:
            user_storage (UserStorage): The user storage
            client_storage (ClientStorage): The client storage
        """
    def create_user(self, api_key: str, identifier: str) -> UserModel:
        """Create user.

        Args:
            api_key (str): The API key for client authentication
            identifier (str): The user identifier

        Returns:
            UserModel: The user model
        """
