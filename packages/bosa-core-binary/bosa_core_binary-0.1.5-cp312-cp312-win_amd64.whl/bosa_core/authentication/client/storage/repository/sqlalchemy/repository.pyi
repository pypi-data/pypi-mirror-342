from _typeshed import Incomplete
from bosa_core.authentication.client.storage.models import ClientBasic as ClientBasic, ClientModel as ClientModel
from bosa_core.authentication.client.storage.repository.base_repository import BaseRepository as BaseRepository
from bosa_core.authentication.client.storage.repository.sqlalchemy.models import DBClient as DBClient
from bosa_core.authentication.database import DatabaseAdapter as DatabaseAdapter
from sqlalchemy.engine import Engine as Engine
from uuid import UUID

class SqlAlchemyClientRepository(BaseRepository):
    """SQLAlchemy client repository."""
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
    def create_client(self, client: ClientBasic) -> ClientModel:
        """Create a client.

        Args:
            client (ClientBasic): The client to create.

        Returns:
            ClientModel: The created client.

        Raises:
            ValidationError: If the data model has changed.
        """
    def get_client_by_id(self, client_id: UUID) -> ClientModel | None:
        """Get a client by ID.

        Args:
            client_id (UUID): The client ID

        Returns:
            ClientModel | None: The client

        Raises:
            ValidationError: If the data model has changed.
        """
