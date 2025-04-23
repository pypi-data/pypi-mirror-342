from typing import TYPE_CHECKING

from knit_langgraph.exceptions.exceptions import KnitException, InvalidKnitAPIKey


if TYPE_CHECKING:
    from knit_langgraph.client.sdk_client import KnitLangGraph


class AuthClient:
    def __init__(self):
        pass

    def initialize_sdk(self, instance: "KnitLangGraph"):
        """
        Initializes the SDK by validating the setup with a GET request.
        Raises:
            InvalidKnitAPIKey: If the API key is invalid.
            KnitException: If any other initialization error occurs.
        """
        try:
            validate_response = instance.http_client.send_request(
                instance, "/sdk.initialize", "GET"
            )

            if validate_response.status_code == 401:
                raise InvalidKnitAPIKey("Invalid API Key")

        except Exception as exc:
            raise KnitException("Error occurred while initializing SDK") from exc
