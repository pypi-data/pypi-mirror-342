import abc
from abc import ABC, abstractmethod
from bosa_core.authentication.plugin.storage.models import ThirdPartyIntegrationAuth as ThirdPartyIntegrationAuth
from uuid import UUID

class ThirdPartyIntegrationStorage(ABC, metaclass=abc.ABCMeta):
    """Third-party integration storage interface."""
    @abstractmethod
    def has_integration(self, client_id: UUID, user_id: UUID, connector: str) -> bool:
        """Returns whether the user has a third-party integration for the specified connector.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.
            connector (str): Connector name.

        Returns:
            bool: True if the user has a third-party integration for the specified connector, False otherwise.
        """
    @abstractmethod
    def get_integration(self, client_id: UUID, user_id: UUID, connector: str) -> ThirdPartyIntegrationAuth | None:
        """Returns the third-party integration for the specified connector.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.
            connector (str): Connector name.

        Returns:
            ThirdPartyIntegrationAuth: Third-party integration, or None if not found.
        """
    @abstractmethod
    def get_integrations(self, client_id: UUID, user_id: UUID) -> list[ThirdPartyIntegrationAuth]:
        """Returns all the third-party integrations for the specified client and user.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.

        Returns:
            List[ThirdPartyIntegrationAuth]: List of third-party integration
        """
    @abstractmethod
    def create_integration(self, integration: ThirdPartyIntegrationAuth):
        """Creates a third-party integration.

        Args:
            integration (ThirdPartyIntegrationAuth): Third-party integration.

        Returns:
            ThirdPartyIntegrationAuth: Created third-party integration.
        """
    @abstractmethod
    def delete_integration(self, client_id: UUID, user_id: UUID, connector: str) -> None:
        """Deletes a third-party integration.

        Args:
            client_id (UUID): Client ID.
            user_id (UUID): User ID.
            connector (str): Connector name.
        """
