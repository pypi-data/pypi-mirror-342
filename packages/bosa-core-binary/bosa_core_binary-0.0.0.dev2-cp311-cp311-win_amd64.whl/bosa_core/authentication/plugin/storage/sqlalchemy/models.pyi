from _typeshed import Incomplete
from bosa_core.authentication.database import DatabaseAdapter as DatabaseAdapter

class DBThirdPartyIntegrationAuth(DatabaseAdapter.base):
    """Third-party integration SQLAlchemy model."""
    __tablename__: str
    __table_args__: Incomplete
    id: Incomplete
    client_id: Incomplete
    user_id: Incomplete
    connector: Incomplete
    user_identifier: Incomplete
    auth_string: Incomplete
    auth_scopes: Incomplete
    client: Incomplete
