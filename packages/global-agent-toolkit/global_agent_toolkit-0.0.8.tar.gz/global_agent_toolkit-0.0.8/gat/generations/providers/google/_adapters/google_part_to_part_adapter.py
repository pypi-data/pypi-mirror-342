from __future__ import annotations

from typing import TYPE_CHECKING, Never

from gat.generations.models.file_part import FilePart
from gat.generations.models.part import Part
from gat.generations.models.text_part import TextPart
from rsb.adapters.adapter import Adapter

if TYPE_CHECKING:
    from google.genai.types import Part as GooglePart


class GooglePartToPartAdapter(Adapter["GooglePart", Part]):
    def adapt(self, _f: GooglePart) -> Part:
        if _f.text:
            return TextPart(text=_f.text)

        if _f.inline_data:
            data = _f.inline_data.data or self._raise_invalid_inline_data(field="data")
            mime_type = _f.inline_data.mime_type or self._raise_invalid_inline_data(
                field="mime_type"
            )
            return FilePart(data=data, mime_type=mime_type)

        raise ValueError(
            f"The provided part: {_f} is not supported by the framework yet."
        )

    def _raise_invalid_inline_data(self, field: str) -> Never:
        raise ValueError(f"Provided field '{field}' is None.")
