import abc

from gat.mcp.models.call_tool_result import CallToolResult
from gat.mcp.tools.mcp_tool import Tool


class MCPServer(abc.ABC):
    """Base class for Model Context Protocol servers."""

    @abc.abstractmethod
    async def connect(self):
        """Connect to the server. For example, this might mean spawning a subprocess or
        opening a network connection. The server is expected to remain connected until
        `cleanup()` is called.
        """
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """A readable name for the server."""
        ...

    @abc.abstractmethod
    async def cleanup(self):
        """Cleanup the server. For example, this might mean closing a subprocess or
        closing a network connection.
        """
        ...

    @abc.abstractmethod
    async def list_tools(self) -> list[Tool]:
        """List the tools available on the server."""
        ...

    @abc.abstractmethod
    async def call_tool(
        self, tool_name: str, arguments: dict[str, object] | None
    ) -> CallToolResult:
        """Invoke a tool on the server."""
        ...
