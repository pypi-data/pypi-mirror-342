from _typeshed import Incomplete
from bosa_core.authentication.client.helper.helper import ClientHelper as ClientHelper
from bosa_core.authentication.client.storage.models import ClientBasic as ClientBasic, ClientModel as ClientModel
from bosa_core.authentication.client.storage.repository.base_repository import BaseRepository as BaseRepository
from uuid import UUID

class ClientStorage:
    """Client storage."""
    repository: Incomplete
    client_helper: Incomplete
    def __init__(self, repository: BaseRepository) -> None:
        """Initialize the storage.

        Args:
            repository (BaseRepository): The repository
        """
    def create_client(self, client: ClientBasic) -> ClientModel:
        """Create client.

        Args:
            client (ClientBasic): The client to create.

        Returns:
            ClientModel: The created client.
        """
    def get_client_by_id(self, client_id: UUID) -> ClientModel:
        """Get client by id.

        Args:
            client_id (UUID): The client ID

        Returns:
            ClientModel: The client
        """
    def get_client_by_api_key(self, api_key: str) -> ClientModel:
        """Get client by API key.

        Args:
            api_key (str): The API key for client authentication

        Returns:
            ClientModel: The client

        Raises:
            InvalidClientException: If the client is not found
        """
