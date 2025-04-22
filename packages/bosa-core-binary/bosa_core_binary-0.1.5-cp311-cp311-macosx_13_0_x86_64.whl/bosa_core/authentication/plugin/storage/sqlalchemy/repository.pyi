from _typeshed import Incomplete
from bosa_core.authentication.database import DatabaseAdapter as DatabaseAdapter
from bosa_core.authentication.plugin.storage.models import ThirdPartyIntegrationAuth as ThirdPartyIntegrationAuth
from bosa_core.authentication.plugin.storage.sqlalchemy.models import DBThirdPartyIntegrationAuth as DBThirdPartyIntegrationAuth
from bosa_core.authentication.plugin.storage.storage import ThirdPartyIntegrationStorage as ThirdPartyIntegrationStorage
from sqlalchemy import Engine as Engine
from uuid import UUID

class SqlAlchemyThirdPartyIntegrationRepository(ThirdPartyIntegrationStorage):
    """SQLAlchemy third-party integration repository."""
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
    def has_integration(self, client_id: UUID, user_id: UUID, connector: str) -> bool:
        """Returns whether the user has a third-party integration for the specified connector.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.
            connector (str): Connector name.

        Returns:
            bool: True if the user has a third-party integration for the specified connector, False otherwise.
        """
    def get_integration(self, client_id: UUID, user_id: UUID, connector: str) -> ThirdPartyIntegrationAuth | None:
        """Returns the third-party integration for the specified connector.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.
            connector (str): Connector name.

        Returns:
            ThirdPartyIntegrationAuth: Third-party integration, or None if not found.
        """
    def get_integrations(self, client_id: UUID, user_id: UUID) -> list[ThirdPartyIntegrationAuth]:
        """Returns all the third-party integrations for the specified connector.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.

        Returns:
            List of third-party integration
        """
    def create_integration(self, integration: ThirdPartyIntegrationAuth) -> ThirdPartyIntegrationAuth:
        """Creates a third-party integration.

        Args:
            integration (ThirdPartyIntegrationAuth): Third-party integration.

        Returns:
            ThirdPartyIntegrationAuth: Created third-party integration.
        """
    def delete_integration(self, client_id: UUID, user_id: UUID, connector: str) -> None:
        """Deletes a third-party integration.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.
            connector (str): Connector name.
        """
