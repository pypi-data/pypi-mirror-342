from collections.abc import Sequence
from typing import override

from gat.generations.models.generation import Generation
from gat.generations.models.message import Message
from gat.generations.services.generations_service_protocol import (
    GenerationsServiceProtocol,
)


class SimpleGenerationService(GenerationsServiceProtocol):
    @override
    async def generate_async[T](
        self,
        model: str,
        messages: Sequence[Message],
        response_schema: type[T] | None = None,
    ) -> Generation[T]:
        return await self.generation_provider.create_generation_async(
            model=model, messages=messages, response_schema=response_schema
        )
