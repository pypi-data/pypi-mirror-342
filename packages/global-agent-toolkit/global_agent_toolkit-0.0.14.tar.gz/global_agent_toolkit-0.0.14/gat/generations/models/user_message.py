from collections.abc import Sequence
from typing import Literal

from gat.generations.models.file_part import FilePart
from gat.generations.models.text_part import TextPart
from gat.generations.models.tool_declaration_part import (
    ToolDeclarationPart,
)
from rsb.models.base_model import BaseModel
from rsb.models.field import Field


class UserMessage(BaseModel):
    parts: Sequence[TextPart | FilePart | ToolDeclarationPart]
    role: Literal["user"] = Field(default="user")
