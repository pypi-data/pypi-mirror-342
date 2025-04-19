from collections.abc import Sequence
from typing import Literal

from gat.generations.models.part import Part
from rsb.decorators.value_objects import valueobject
from rsb.models.base_model import BaseModel
from rsb.models.field import Field


@valueobject
class RawPartsResponse(BaseModel):
    raw_parts: Sequence[Part] = Field(description="Just the raw LLM output.")

    def __bool__(self) -> Literal[False]:
        return False
