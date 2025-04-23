from typing import TYPE_CHECKING, Optional, Union
import httpx

from knit_langgraph.exceptions.exceptions import KnitException
from knit_langgraph.utils.constants import (
    ENVIRONMENT_LOCAL,
    ENVIRONMENT_PRODUCTION,
    ENVIRONMENT_SANDBOX,
    VERSION,
)
from knit_langgraph.logger import knit_logger

if TYPE_CHECKING:
    from knit_langgraph.client.sdk_client import KnitLangGraph


class HTTPClient:
    """
    A client for handling HTTP requests to the Knit API.

    This class is responsible for making HTTP requests to the specified
    environment. It supports different environments (sandbox, production, local),
    adds authentication headers, and processes responses.

    Attributes:
        environment (str): The environment to be used by the client.
        base_url (str): The base URL for HTTP requests based on the environment.
        client (httpx.Client): The HTTP client used for sending requests.
    """

    def __init__(self, environment: str):
        """
        Initialize the HTTPClient instance with the specified environment.

        Args:
            environment (str): The environment to use, should be one of
                ENVIRONMENT_SANDBOX, ENVIRONMENT_PRODUCTION, or ENVIRONMENT_LOCAL.

        Raises:
            KnitException: If the provided environment is invalid.
        """
        knit_logger.debug("Initializing HTTPClient with environment: %s", environment)

        if environment == ENVIRONMENT_SANDBOX:
            self.base_url = "https://sdk-service.sandbox.getknit.dev"
        elif environment == ENVIRONMENT_PRODUCTION:
            self.base_url = "https://sdk-service.getknit.dev"
        elif environment == ENVIRONMENT_LOCAL:
            self.base_url = "http://localhost:1328"
        else:
            knit_logger.error("Invalid environment: %s", environment)
            raise KnitException("Invalid environment")

        knit_logger.debug("Using base URL: %s", self.base_url)
        self.client = httpx.Client(timeout=60.0)

    def add_auth_headers(
        self, instance: "KnitLangGraph", request: httpx.Request
    ) -> httpx.Request:
        """
        Add authentication headers to an HTTP request.

        This method adds necessary authorization headers to a given HTTP request
        using the API key associated with the provided KnitLangGraph instance.

        Args:
            instance (KnitLangGraph): The instance containing the API key for authorization.
            request (httpx.Request): The HTTP request object to which headers are added.

        Returns:
            httpx.Request: The modified request with added authentication headers.
        """
        knit_logger.debug("Adding authentication headers to request")

        request.headers["Authorization"] = f"Bearer {instance.api_key}"
        request.headers["X-Source"] = "knit-langgraph-sdk"
        request.headers["X-SDK-Version"] = VERSION

        return request

    def send_request(
        self,
        instance: "KnitLangGraph",
        url: str,
        method: str,
        validate_response: bool = True,
        params: dict | None = None,
        json_body: dict | None = None,
        knit_integration_id: str | None = None,
    ) -> httpx.Response:
        """
        Send an HTTP request using the configured client.

        This method creates and sends an HTTP request to the specified URL with the
        given method, parameters, and JSON body. It includes authentication
        headers and validates the response if requested.

        Args:
            instance (KnitLangGraph): The instance containing the API key for authorization.
            url (str): The URL endpoint to which the request is sent.
            method (str): The HTTP method (GET, POST, etc.) to use for the request.
            validate_response (bool, optional): Whether to validate the response status code. Defaults to True.
            params (dict, optional): Query parameters to include in the request. Defaults to None.
            json_body (dict, optional): JSON body to include in the request. Defaults to None.
            knit_integration_id (str, optional): A specific integration ID to use for this request. Defaults to None.

        Returns:
            httpx.Response: The HTTP response object if the request is successful.

        Raises:
            KnitException: If validate_response is True and the request does not return a status code of 200.
        """
        full_url = f"{self.base_url}{url}"
        knit_logger.debug("Preparing %s request to %s", method, full_url)
        if params:
            knit_logger.debug("Request params: %s", params)
        if json_body:
            knit_logger.debug("Request body: %s", json_body)

        request = httpx.Request(
            method=method, url=full_url, params=params, json=json_body
        )
        request = self.add_auth_headers(instance, request)

        # Add integration_id header if provided
        if knit_integration_id:
            knit_logger.debug("Using provided integration_id: %s", knit_integration_id)
            request.headers["X-Knit-Integration-Id"] = knit_integration_id
        elif instance.integration_id:
            knit_logger.debug(
                "Using instance integration_id: %s", instance.integration_id
            )
            request.headers["X-Knit-Integration-Id"] = instance.integration_id

        try:
            knit_logger.debug("Sending %s request to %s", method, url)
            response = self.client.send(request)
            knit_logger.debug(
                "Received response with status code: %d", response.status_code
            )

            if validate_response:
                if response.status_code != 200:
                    error_content = response.json()
                    knit_logger.error(
                        "API call failed with status %d: %s",
                        response.status_code,
                        error_content,
                    )
                    raise KnitException(
                        f"Error Occurred while making API Call : {error_content}"
                    )

            return response
        except httpx.RequestError as e:
            knit_logger.error(
                "Network error when making request to %s: %s", url, str(e)
            )
            raise KnitException(f"Network error: {str(e)}")
        except Exception as e:
            knit_logger.error("Error sending request to %s: %s", url, str(e))
            raise
