import abc
from collections.abc import Sequence

from gat.generations.models.developer_message import DeveloperMessage
from gat.generations.models.file_part import FilePart
from gat.generations.models.generation import Generation
from gat.generations.models.generation_config import GenerationConfig
from gat.generations.models.message import Message
from gat.generations.models.part import Part
from gat.generations.models.raw_parts_response import RawPartsResponse
from gat.generations.models.text_part import TextPart
from gat.generations.models.user_message import UserMessage
from gat.generations.tracing.contracts.stateful_observability_client import (
    StatefulObservabilityClient,
)
from gat.prompts.models.prompt import Prompt
from rsb.contracts.maybe_protocol import MaybeProtocol
from rsb.coroutines.run_sync import run_sync
from rsb.containers.maybe import Maybe


class GenerationProvider(abc.ABC):
    tracing_client: MaybeProtocol[StatefulObservabilityClient]

    def __init__(
        self,
        tracing_client: StatefulObservabilityClient | None = None,
    ) -> None:
        self.tracing_client = Maybe(tracing_client)

    def create_generation_by_prompt[T = RawPartsResponse](
        self,
        *,
        model: str,
        prompt: str | Prompt | Part | Sequence[Part],
        developer_prompt: str | Prompt,
        response_schema: type[T] | None = None,
        generation_config: GenerationConfig | None = None,
    ):
        return run_sync(
            self.create_generation_by_prompt_async,
            model=model,
            prompt=prompt,
            developer_prompt=developer_prompt,
            response_schema=response_schema,
            generation_config=generation_config,
        )

    async def create_generation_by_prompt_async[T = RawPartsResponse](
        self,
        *,
        model: str,
        prompt: str | Prompt | Part | Sequence[Part],
        developer_prompt: str | Prompt,
        response_schema: type[T] | None = None,
        generation_config: GenerationConfig | None = None,
    ):
        user_message_parts: Sequence[Part]
        match prompt:
            case str():
                user_message_parts = [TextPart(text=prompt)]
            case Prompt():
                user_message_parts = [TextPart(text=prompt.content)]
            case TextPart():
                user_message_parts = [prompt]
            case FilePart():
                user_message_parts = [prompt]
            case _:
                user_message_parts = prompt

        developer_message_parts: Sequence[Part]
        match developer_prompt:
            case str():
                developer_message_parts = [TextPart(text=developer_prompt)]
            case Prompt():
                developer_message_parts = [TextPart(text=developer_prompt.content)]

        user_message = UserMessage(parts=user_message_parts)
        developer_message = DeveloperMessage(parts=developer_message_parts)

        return self.create_generation(
            model=model,
            messages=[developer_message, user_message],
            response_schema=response_schema,
            generation_config=generation_config,
        )

    def create_generation[T = RawPartsResponse](
        self,
        *,
        model: str,
        messages: Sequence[Message],
        response_schema: type[T] | None = None,
        generation_config: GenerationConfig | None = None,
    ) -> Generation[T]:
        return run_sync(
            self.create_generation_async,
            model=model,
            messages=messages,
            response_schema=response_schema,
            generation_config=generation_config,
        )

    @abc.abstractmethod
    async def create_generation_async[T = RawPartsResponse](
        self,
        *,
        model: str,
        messages: Sequence[Message],
        response_schema: type[T] | None = None,
        generation_config: GenerationConfig | None = None,
    ) -> Generation[T]: ...
