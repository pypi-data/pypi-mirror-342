from _typeshed import Incomplete
from bosa_core.authentication.client.helper.helper import ClientHelper as ClientHelper
from bosa_core.authentication.client.storage.client_storage import ClientStorage as ClientStorage
from bosa_core.authentication.client.storage.models import Client as Client, ClientBasic as ClientBasic

class CreateClientService:
    """Service for creating clients."""
    client_storage: Incomplete
    client_helper: Incomplete
    def __init__(self, client_storage: ClientStorage) -> None:
        """Initialize the service.

        Args:
            client_storage (ClientStorage): The client storage
        """
    def create_client(self, client_name: str) -> Client:
        """Create client.

        Args:
            client_name (str): The name of the client

        Returns:
            Client: The created client
        """
