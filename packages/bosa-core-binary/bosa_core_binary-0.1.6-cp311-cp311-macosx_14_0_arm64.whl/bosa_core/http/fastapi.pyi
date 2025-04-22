from ..api.response import ApiResponse as ApiResponse
from .auth.schema import AuthenticationSchema as AuthenticationSchema
from .fastapi_schema import FastApiSchemaExtractor as FastApiSchemaExtractor
from .header import ExposedDefaultHeaders as ExposedDefaultHeaders, HttpHeaders as HttpHeaders
from .input import InputFile as InputFile
from .interface import HttpInterface as HttpInterface, SchemaExtractor as SchemaExtractor
from .router import Router as Router
from fastapi import FastAPI as FastAPI, Request as Request

class FastApiHttpInterface(HttpInterface):
    """FastAPI HTTP interface."""
    def __init__(self, app: FastAPI, base_api_prefix: str = '/api', authentication_schema: AuthenticationSchema = None) -> None:
        '''Constructor.

        Args:
            app (FastAPI): The FastAPI app
            base_api_prefix (str, optional): The base API prefix. Defaults to "/api".
            authentication_schema (AuthenticationSchema, optional): The authentication schema. Defaults to None.
        '''
    def handle_routing(self, prefix: str, router: Router):
        """Register routes with the FastAPI app.

        Args:
            prefix: The prefix for the routes
            router: The router instance
        """
    def get_schema_extractor(self) -> SchemaExtractor:
        """Get the schema extractor for this interface.

        Returns:
            SchemaExtractor implementation for this interface
        """
