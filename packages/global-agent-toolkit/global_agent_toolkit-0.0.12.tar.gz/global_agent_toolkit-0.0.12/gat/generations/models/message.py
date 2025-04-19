from typing import Annotated

from gat.generations.models.assistant_message import AssistantMessage
from gat.generations.models.developer_message import DeveloperMessage
from gat.generations.models.user_message import UserMessage
from rsb.models.field import Field

type Message = Annotated[
    AssistantMessage | DeveloperMessage | UserMessage, Field(discriminator="role")
]
