from __future__ import annotations

import abc
from collections.abc import Sequence

from gat.generations.models.generation import Generation
from gat.generations.models.message import Message
from gat.generations.models.raw_parts_response import RawPartsResponse
from gat.generations.providers import GenerationProvider
from rsb.coroutines.run_sync import run_sync
from rsb.decorators.services import abstractservice


@abstractservice
class GenerationsServiceProtocol(abc.ABC):
    generation_provider: GenerationProvider

    def __init__(
        self,
        generation_strategy: GenerationProvider,
    ) -> None:
        self.generation_provider = generation_strategy

    def generate[T = RawPartsResponse](
        self,
        model: str,
        messages: Sequence[Message],
        response_schema: type[T] | None = None,
    ) -> Generation[T]:
        return run_sync(
            self.generate_async,
            timeout=None,
            model=model,
            messages=messages,
            response_schema=response_schema,
        )

    @abc.abstractmethod
    async def generate_async[T = RawPartsResponse](
        self,
        model: str,
        messages: Sequence[Message],
        response_schema: type[T] | None = None,
    ) -> Generation[T]: ...
