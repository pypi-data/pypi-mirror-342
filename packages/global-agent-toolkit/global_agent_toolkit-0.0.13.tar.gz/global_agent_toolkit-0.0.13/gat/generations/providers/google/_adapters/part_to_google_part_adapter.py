from __future__ import annotations

from typing import TYPE_CHECKING

from gat.generations.models.file_part import FilePart
from gat.generations.models.part import Part
from gat.generations.models.text_part import TextPart
from rsb.adapters.adapter import Adapter

if TYPE_CHECKING:
    from google.genai.types import Part as GooglePart


class PartToGooglePartAdapter(Adapter[Part, "GooglePart"]):
    def adapt(self, _f: Part) -> GooglePart:
        from google.genai.types import Blob
        from google.genai.types import Part as GooglePart

        match _f:
            case TextPart():
                return GooglePart(text=_f.text)
            case FilePart():
                return GooglePart(
                    inline_data=Blob(data=_f.data, mime_type=_f.mime_type)
                )
            case _:
                pass
