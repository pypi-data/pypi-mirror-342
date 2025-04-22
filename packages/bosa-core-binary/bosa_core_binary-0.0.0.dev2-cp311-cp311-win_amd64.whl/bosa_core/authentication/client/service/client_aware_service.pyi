from _typeshed import Incomplete
from abc import ABC
from bosa_core.authentication.client.helper.helper import ClientHelper as ClientHelper
from bosa_core.authentication.client.service.verify_client_service import VerifyClientService as VerifyClientService
from bosa_core.authentication.client.storage.client_storage import ClientStorage as ClientStorage
from bosa_core.authentication.client.storage.models import ClientModel as ClientModel
from bosa_core.exception import InvalidClientException as InvalidClientException

class ClientAwareService(ABC):
    """Services marked by this abstract class are client-aware.

    These services will have access to the client information via the `get_client` method.
    """
    client_storage: Incomplete
    verify_client_service: Incomplete
    client_helper: Incomplete
    def __init__(self, client_storage: ClientStorage) -> None:
        """Initialize the service.

        Args:
            client_storage (ClientStorage): The client storage
        """
    def get_client(self, api_key: str) -> ClientModel:
        """Get client by API key.

        Args:
            api_key (str): The API key for client authentication

        Returns:
            ClientModel: The client

        Raises:
            InvalidClientException: If the client is not found
        """
