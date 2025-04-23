import os
import json
from typing import Any

from langchain_core.tools import StructuredTool
from langchain_core.runnables.config import RunnableConfig

from knit_langgraph.exceptions.exceptions import InvalidKnitAPIKey
from knit_langgraph.models.tools_filter import ToolFilter
from knit_langgraph.models.tools_summary import ToolSummary
from knit_langgraph.utils.constants import ENVIRONMENT_PRODUCTION
from knit_langgraph.client.http_client import HTTPClient
from knit_langgraph.client.auth_client import AuthClient
from knit_langgraph.logger import knit_logger


class KnitLangGraph:
    """
    A client for interfacing with the Knit LangGraph API.

    This client handles authentication and manages interactions with the Knit API
    for LangGraph integrations, allowing tool discovery and execution.
    """

    _api_key: str
    _http_client: HTTPClient = None
    _auth_client: AuthClient = None
    integration_id: str
    environment: str = ENVIRONMENT_PRODUCTION

    def __init__(
        self,
        api_key: str | None = None,
        integration_id: str | None = None,
        environment: str | None = None,
    ):
        """
        Initialize a new instance of the KnitLangGraph client.

        Args:
            api_key (str, optional): The API key used for authenticating requests.
                If not provided, it will attempt to read from the KNIT_API_KEY environment variable.
            integration_id (str, optional): The integration ID associated with this client.
            environment (str, optional): The API environment to connect to, defaulting to production if not specified.

        Raises:
            InvalidKnitAPIKey: If the api_key is not provided either by argument or environment variable.
        """
        knit_logger.debug("Initializing KnitLangGraph client")

        if api_key is None:
            knit_logger.debug("API key not provided, checking environment variable")
            api_key = os.environ.get("KNIT_API_KEY")

        if api_key is None:
            knit_logger.error(
                "API key not found in environment variable or constructor argument"
            )
            raise InvalidKnitAPIKey(
                "The api_key must be set either by passing api_key to the SDK or by setting the KNIT_API_KEY environment variable"
            )
        self._api_key = api_key

        self.environment = environment
        self.integration_id = integration_id
        knit_logger.debug(
            "KnitLangGraph client initialized with environment: %s, integration_id: %s",
            environment,
            integration_id,
        )

        self.auth_client.initialize_sdk(self)
        knit_logger.debug("Auth client initialized")

    @property
    def auth_client(self) -> AuthClient:
        """
        Get the authentication client for managing API interactions.

        If the authentication client has not been instantiated, it creates one.

        Returns:
            AuthClient: The authentication client instance for handling authorization.
        """
        if not self._auth_client:
            knit_logger.debug("Creating new AuthClient instance")
            self._auth_client = AuthClient()

        return self._auth_client

    @property
    def api_key(self) -> str:
        """
        Get the API key used for authenticating requests.

        Returns:
            str: The API key.

        Raises:
            InvalidKnitAPIKey: If the API key is not set.
        """
        if not self._api_key:
            knit_logger.error("API key not set when attempting to access it")
            raise InvalidKnitAPIKey(
                "The api_key must be set either by passing api_key to the SDK or by setting the KNIT_API_KEY environment variable"
            )
        return self._api_key

    @property
    def http_client(self) -> HTTPClient:
        """
        Get the HTTP client for making API requests.

        If the HTTP client hasn't been instantiated, it creates one using the current environment setting.

        Returns:
            HTTPClient: The HTTP client instance for handling requests.
        """
        if not self._http_client:
            knit_logger.debug(
                "Creating new HTTPClient instance with environment: %s",
                self.environment,
            )
            self._http_client = HTTPClient(self.environment)

        return self._http_client

    def find_tools(
        self,
        app_id: str | None = None,
        entities: list[str] | None = None,
        operation: str | None = None,
        category_id: str | None = None,
        include_unified_tools: bool = False,
        usecase: str | None = None,
    ) -> list[ToolSummary]:
        """
        Find and retrieve a list of tool summaries based on specified filters.

        This method fetches tools that match given criteria and returns them as ToolSummary objects.

        Args:
            app_id (str, optional): The application ID for which tools are being retrieved.
            entities (list[str], optional): A list of entities to filter the tools.
            operation (str, optional): An operation name to filter the tools.
                Allowed values are "read" and "write".
            category_id (str, optional): A category ID to filter the tools.
                Must be specified if app_id is not provided.
            include_unified_tools (bool, optional): Whether to include unified tools.
                Defaults to False.
            usecase (str, optional): Search for tools by a semantic search.

        Returns:
            list[ToolSummary]: A list of ToolSummary objects representing the tools
                that match the specified filters.

        Raises:
            Exception: If an error occurs during the API request.
        """
        knit_logger.debug(
            "Finding tools with filters - app_id: %s, entities: %s, operation: %s, category_id: %s, include_unified_tools: %s, usecase: %s",
            app_id,
            entities,
            operation,
            category_id,
            include_unified_tools,
            usecase,
        )

        filter_obj = {
            **({"app_id": app_id} if app_id is not None else {}),
            **({"entities": entities} if entities is not None else {}),
            **({"operation": operation} if operation is not None else {}),
            **({"category_id": category_id} if category_id is not None else {}),
            **({"usecase": usecase} if usecase is not None else {}),
            **(
                {"include_unified_tools": include_unified_tools}
                if include_unified_tools
                else {}
            ),
        }

        try:
            knit_logger.debug(
                "Sending request to /tools.find with filters: %s", filter_obj
            )
            response = self.http_client.send_request(
                instance=self,
                url="/tools.find",
                method="GET",
                validate_response=True,
                params=None,
                json_body={"filters": filter_obj},
            )

            data = response.json()["data"]
            knit_logger.debug("Retrieved %d tools from /tools.find", len(data))

            tools = []
            for tool in data:
                tools.append(
                    ToolSummary(
                        tool_id=tool["tool_id"],
                        entities=tool["entities"],
                        operation=tool["operation"],
                        title=tool["title"],
                        description=tool["description"],
                        is_unified_tool=tool["is_unified_tool"],
                    )
                )

            return tools
        except Exception as e:
            knit_logger.error("Error finding tools: %s", str(e))
            raise

    def execute_tool_call(
        self, function_id: str, knit_integration_id: str | list[str], arguments: dict
    ) -> Any:
        """
        Execute a tool call with the provided parameters.

        This method sends a request to execute a specific tool function with the given arguments.

        Args:
            function_id (str): The unique identifier of the function to execute.
            knit_integration_id (str): The integration ID for the current execution context.
            arguments (dict): The arguments to pass to the function.

        Returns:
            Any: The result of the tool execution.

        Raises:
            Exception: If an error occurs during the API request or tool execution.
        """
        knit_logger.debug(
            "Executing tool call - function_id: %s, knit_integration_id: %s",
            function_id,
            knit_integration_id,
        )

        body = {
            "function_id": function_id,
            "arguments": json.dumps(arguments),
            "knit_integration_id": knit_integration_id
        }

        try:
            knit_logger.debug("Sending request to /tools.execute with body: %s", body)
            response = self.http_client.send_request(
                instance=self,
                url="/tools.execute",
                method="POST",
                validate_response=True,
                params=None,
                json_body=body,
                knit_integration_id=None,
            )

            data = response.json()["data"]
            knit_logger.debug(
                "Tool execution completed for function_id: %s", function_id
            )

            return data
        except Exception as e:
            knit_logger.error(
                "Error executing tool call for function_id %s: %s", function_id, str(e)
            )
            raise

    def create_function(self, tool_data: dict) -> callable:
        """
        Create a callable function from tool data.

        This method creates a function that can be called to execute the specified tool.

        Args:
            tool_data (dict): Data describing the tool, including name and description.

        Returns:
            callable: A function that when called will execute the tool with
                the provided arguments.
        """
        knit_logger.debug("Creating function for tool: %s", tool_data["name"])

        def function(config: RunnableConfig, **kwargs: Any) -> Any:
            """
            Execute the tool with the provided arguments.

            Args:
                config (RunnableConfig): Configuration for the execution, including
                    the knit_integration_id.
                **kwargs: Arguments to pass to the tool.

            Returns:
                Any: The result of the tool execution.

            Raises:
                KeyError: If the required configuration is missing.
                Exception: If an error occurs during tool execution.
            """
            knit_logger.debug("Invoking %s with args: %s", tool_data["name"], kwargs)

            try:
                integration_id = config["configurable"]["knit_integration_id"]
                knit_logger.debug("Using integration_id: %s", integration_id)

                result = self.execute_tool_call(
                    tool_data["name"], integration_id, kwargs
                )
                return result
            except KeyError as e:
                knit_logger.error(
                    "Missing required configuration for %s: %s",
                    tool_data["name"],
                    str(e),
                )
                raise
            except Exception as e:
                knit_logger.error("Error executing %s: %s", tool_data["name"], str(e))
                raise

        return function

    def get_tools(self, tools: list[ToolFilter]) -> list[StructuredTool]:
        """
        Retrieve a list of tools based on the specified filters.

        This method fetches tools matching the given filters and converts them to
        LangChain StructuredTool objects that can be used with LangGraph.

        Args:
            tools (list[ToolFilter]): A list of ToolFilter objects representing the
                criteria for tools to retrieve.

        Returns:
            list[StructuredTool]: A list of LangChain StructuredTool objects representing
                the tools that match the specified filters.

        Raises:
            Exception: If an error occurs during the API request or tool processing.
        """
        knit_logger.debug("Getting tools with %d filter(s)", len(tools))

        filter_obj = [tool.model_dump(exclude_none=True) for tool in tools]
        knit_logger.debug("Tool filters: %s", filter_obj)

        try:
            knit_logger.debug("Sending request to /tools.get")
            response = self.http_client.send_request(
                instance=self,
                url="/tools.get",
                method="POST",
                validate_response=True,
                params=None,
                json_body={"filters": filter_obj},
            )

            data = response.json()["data"]
            knit_logger.debug("Retrieved %d tools from /tools.get", len(data))

            tools = []
            for tool in data:
                knit_logger.debug("Processing tool: %s", tool["id"])

                function = self.create_function(tool)

                function.__name__ = tool["id"]
                function.__doc__ = tool["description"]

                structured_tool = StructuredTool.from_function(
                    func=function,
                    name=tool["id"],
                    description=tool["description"],
                    args_schema=tool.get("parameters", {}),
                )

                tools.append(structured_tool)
                knit_logger.debug("Added tool: %s", tool["id"])

            return tools
        except Exception as e:
            knit_logger.error("Error getting tools: %s", str(e))
            raise
