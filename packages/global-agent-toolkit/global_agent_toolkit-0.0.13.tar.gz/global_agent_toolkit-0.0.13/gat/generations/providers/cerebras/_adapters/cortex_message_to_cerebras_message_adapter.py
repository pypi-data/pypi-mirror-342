from cerebras.cloud.sdk.types.chat.completion_create_params import (
    MessageAssistantMessageRequestTyped,
    MessageSystemMessageRequestTyped,
    MessageUserMessageRequestTyped,
)

from gat.generations.models.assistant_message import AssistantMessage
from gat.generations.models.developer_message import DeveloperMessage
from gat.generations.models.user_message import UserMessage
from rsb.adapters.adapter import Adapter


class CortexMessageToCerebrasMessageAdapter(
    Adapter[
        AssistantMessage | DeveloperMessage | UserMessage,
        MessageSystemMessageRequestTyped
        | MessageAssistantMessageRequestTyped
        | MessageUserMessageRequestTyped,
    ]
):
    def adapt(
        self, _f: AssistantMessage | DeveloperMessage | UserMessage
    ) -> (
        MessageSystemMessageRequestTyped
        | MessageAssistantMessageRequestTyped
        | MessageUserMessageRequestTyped
    ):
        match _f:
            case AssistantMessage():
                return MessageAssistantMessageRequestTyped(
                    role="assistant", content="".join(p.text for p in _f.parts)
                )
            case DeveloperMessage():
                return MessageSystemMessageRequestTyped(
                    role="system", content="".join(p.text for p in _f.parts)
                )
            case UserMessage():
                return MessageUserMessageRequestTyped(
                    role="user", content="".join(p.text for p in _f.parts)
                )
