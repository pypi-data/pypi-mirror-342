from collections.abc import Sequence
import random

from gat.generations.models.generation_config import GenerationConfig
from gat.generations.models.generation import Generation
from gat.generations.models.message import Message
from gat.generations.models.raw_parts_response import RawPartsResponse
from gat.generations.providers.base.generation_provider import (
    GenerationProvider,
)
from gat.generations.tracing.contracts.stateful_observability_client import (
    StatefulObservabilityClient,
)
from rsb.contracts.maybe_protocol import MaybeProtocol


class FailoverGenerationProvider(GenerationProvider):
    generation_providers: Sequence[GenerationProvider]
    tracing_client: MaybeProtocol[StatefulObservabilityClient]
    shuffle: bool

    def __init__(
        self,
        tracing_client: StatefulObservabilityClient | None,
        generation_providers: Sequence[GenerationProvider],
        shuffle: bool = False,
    ) -> None:
        super().__init__(tracing_client=tracing_client)
        self.generation_providers = generation_providers
        self.shuffle = shuffle
    async def create_generation_async[T = RawPartsResponse](
        self,
        *,
        model: str,
        messages: Sequence[Message],
        response_schema: type[T] | None = None,
        generation_config: GenerationConfig | None = None,
    ) -> Generation[T]:
        exceptions: list[Exception] = []

        providers = list(self.generation_providers)
        if self.shuffle:
            random.shuffle(providers)

        for provider in providers:
            try:
                return await provider.create_generation_async(
                    model=model,
                    messages=messages,
                    response_schema=response_schema,
                    generation_config=generation_config,
                )
            except Exception as e:
                exceptions.append(e)
                continue

        if not exceptions:
            raise RuntimeError("Exception is None and the for loop went out.")

        raise exceptions[0]
