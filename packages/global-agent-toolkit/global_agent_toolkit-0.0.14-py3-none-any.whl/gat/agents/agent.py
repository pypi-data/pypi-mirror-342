from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from gat.agents.agent_config import AgentConfig
from gat.agents.agent_instructions import AgentInstructions
from gat.agents.agent_run_response import AgentRunResponse
from gat.agents.models.context import Context
from gat.agents.pipelines.agent_pipeline import AgenticPipeline
from gat.agents.squads.agent_squad import AgentSquad
from gat.generations.models.message import Message
from gat.generations.models.part import Part
from gat.generations.models.user_message import UserMessage
from gat.generations.providers.base.generation_provider import (
    GenerationProvider,
)
from gat.generations.tools.tool import Tool as GenerationTool
from gat.mcp.servers.mcp_server import MCPServer
from gat.mcp.tools.mcp_tool import Tool as MCPTool
from rsb.coroutines.run_sync import run_sync
from rsb.models.base_model import BaseModel


class Agent[T = str](BaseModel):
    name: str
    description: str
    instructions: (
        str
        | Callable[[], str]
        | Callable[[Context], str]
        | Sequence[str]
        | AgentInstructions
    )
    response_schema: type[T]
    generation_provider: GenerationProvider
    model: str
    mcp_servers: Sequence[MCPServer]
    tools: Sequence[Callable[..., object] | GenerationTool | MCPTool]
    config: AgentConfig

    def run(
        self,
        input: str
        | Context
        | Sequence[Message]
        | UserMessage
        | Part
        | Sequence[Part]
        | Callable[[], str],
    ) -> AgentRunResponse[T]:
        return run_sync(self.run_async, timeout=None, input=input)

    async def run_async(
        self,
        input: str
        | Context
        | Sequence[Message]
        | UserMessage
        | Part
        | Sequence[Part]
        | Callable[[], str]
        | Callable[[Context], str],
    ) -> AgentRunResponse[T]: ...

    def __add__(self, other: Agent[Any]) -> AgentSquad: ...

    def __or__(self, other: Agent) -> AgenticPipeline: ...
