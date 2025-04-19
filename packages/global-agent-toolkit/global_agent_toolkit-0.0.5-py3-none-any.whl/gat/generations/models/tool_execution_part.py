from typing import Literal
from rsb.models.base_model import BaseModel
from rsb.models.field import Field


class ToolExecutionPart(BaseModel):
    type: Literal["tool_execution"] = Field(
        default="tool_execution",
    )
    tool_name: str
    args: dict[str, object] = Field(default_factory=dict)
