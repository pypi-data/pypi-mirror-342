from typing import Literal
from rsb.models.base_model import BaseModel
from rsb.models.field import Field


class ToolDeclarationPart(BaseModel):
    type: Literal["tool_declaration"] = Field(default="tool_declaration")
    name: str
