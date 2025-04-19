from typing import Literal, Sequence

from gat.generations.models.part import Part
from rsb.decorators.value_objects import valueobject
from rsb.models.base_model import BaseModel
from rsb.models.field import Field


@valueobject
class DeveloperMessage(BaseModel):
    parts: Sequence[Part]
    role: Literal["developer"] = Field(default="developer")
