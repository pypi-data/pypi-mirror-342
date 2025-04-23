from _typeshed import Incomplete
from pydantic import BaseModel
from uuid import UUID

class ThirdPartyIntegrationAuthBasic(BaseModel):
    """Third-party integration auth basic model."""
    id: UUID | None
    client_id: UUID
    user_id: UUID
    connector: str
    user_identifier: str

class ThirdPartyIntegrationAuth(ThirdPartyIntegrationAuthBasic):
    """Third-party integration auth model."""
    model_config: Incomplete
    id: UUID | None
    client_id: UUID
    user_id: UUID
    connector: str
    user_identifier: str
    auth_string: str
    auth_scopes: list[str]
