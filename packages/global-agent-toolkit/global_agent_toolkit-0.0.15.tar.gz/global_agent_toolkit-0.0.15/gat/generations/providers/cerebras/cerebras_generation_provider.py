import datetime
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, cast, override

import httpx

from gat.generations.json.schema_builder import SchemaBuilder
from gat.generations.models.assistant_message import AssistantMessage
from gat.generations.models.developer_message import DeveloperMessage
from gat.generations.models.generation import Generation
from gat.generations.models.generation_config import GenerationConfig
from gat.generations.models.raw_parts_response import RawPartsResponse
from gat.generations.models.user_message import UserMessage
from gat.generations.pricing.price_retrievable import PriceRetrievable
from gat.generations.providers.cerebras._adapters.completion_to_generation_adapter import (
    CerebrasCompletionToGenerationAdapter,
)
from gat.generations.providers.cerebras._adapters.cortex_message_to_cerebras_message_adapter import (
    CortexMessageToCerebrasMessageAdapter,
)
from gat.generations.providers.base.generation_provider import (
    GenerationProvider,
)
from rsb.adapters.adapter import Adapter

if TYPE_CHECKING:
    from cerebras.cloud.sdk.types.chat.completion_create_params import (
        MessageAssistantMessageRequestTyped,
        MessageSystemMessageRequestTyped,
        MessageUserMessageRequestTyped,
    )


class CerebrasGenerationProvider(GenerationProvider, PriceRetrievable):
    api_key: str | None
    base_url: str | httpx.URL | None
    timeout: float | httpx.Timeout | None
    max_retries: int
    default_headers: Mapping[str, str] | None
    default_query: Mapping[str, object] | None
    http_client: httpx.AsyncClient | None
    _strict_response_validation: bool
    warm_tcp_connection: bool
    message_adapter: Adapter[
        AssistantMessage | UserMessage | DeveloperMessage,
        MessageSystemMessageRequestTyped
        | MessageAssistantMessageRequestTyped
        | MessageUserMessageRequestTyped,
    ]

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | httpx.Timeout | None,
        max_retries: int = 2,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        _strict_response_validation: bool = False,
        warm_tcp_connection: bool = True,
        message_adapter: Adapter[
            AssistantMessage | UserMessage | DeveloperMessage,
            MessageSystemMessageRequestTyped
            | MessageAssistantMessageRequestTyped
            | MessageUserMessageRequestTyped,
        ]
        | None = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client
        self._strict_response_validation = _strict_response_validation
        self.warm_tcp_connection = warm_tcp_connection
        self.message_adapter = (
            message_adapter or CortexMessageToCerebrasMessageAdapter()
        )

    @override
    async def create_generation_async[T = RawPartsResponse](
        self,
        *,
        model: str,
        messages: Sequence[AssistantMessage | DeveloperMessage | UserMessage],
        response_schema: type[T] | None = None,
        generation_config: GenerationConfig | None = None,
    ) -> Generation[T]:
        from cerebras.cloud.sdk import AsyncCerebras
        from cerebras.cloud.sdk.types.chat.chat_completion import ChatCompletionResponse

        start = datetime.datetime.now()

        client = AsyncCerebras(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            max_retries=self.max_retries,
            default_headers=self.default_headers,
            default_query=self.default_query,
            http_client=self.http_client,
            _strict_response_validation=self._strict_response_validation,
            warm_tcp_connection=self.warm_tcp_connection,
        )

        cerebras_completion = cast(
            ChatCompletionResponse,
            await client.chat.completions.create(
                messages=[self.message_adapter.adapt(message) for message in messages],
                model=model,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "json_schema",
                        "strict": True,
                        "schema": SchemaBuilder(response_schema).build(
                            dereference=True
                        ),
                    },
                }
                if response_schema
                else None,
                stream=False,
            ),
        )

        return CerebrasCompletionToGenerationAdapter[T](
            response_schema=response_schema, start_time=start, model=model
        ).adapt(cerebras_completion)

    @override
    def price_per_million_tokens_input(
        self, model: str, estimate_tokens: int | None = None
    ) -> float:
        return 0.0  # TODO(arthur)

    @override
    def price_per_million_tokens_output(
        self, model: str, estimate_tokens: int | None = None
    ) -> float:
        return 0.0  # TODO(arthur)
