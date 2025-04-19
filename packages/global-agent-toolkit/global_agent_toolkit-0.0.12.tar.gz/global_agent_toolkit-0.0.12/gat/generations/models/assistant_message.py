from typing import Literal, Sequence

from gat.generations.models.file_part import FilePart
from gat.generations.models.text_part import TextPart
from gat.generations.models.tool_execution_part import ToolExecutionPart
from rsb.decorators.value_objects import valueobject
from rsb.models.base_model import BaseModel
from rsb.models.field import Field


@valueobject
class AssistantMessage(BaseModel):
    parts: Sequence[TextPart | FilePart | ToolExecutionPart]
    role: Literal["assistant"] = Field(default="assistant")
