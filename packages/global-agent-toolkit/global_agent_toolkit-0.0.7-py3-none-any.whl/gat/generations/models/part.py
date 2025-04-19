from typing import Annotated

from gat.generations.models.file_part import FilePart
from gat.generations.models.text_part import TextPart
from rsb.models.field import Field

type Part = Annotated[TextPart | FilePart, Field(discriminator="type")]
