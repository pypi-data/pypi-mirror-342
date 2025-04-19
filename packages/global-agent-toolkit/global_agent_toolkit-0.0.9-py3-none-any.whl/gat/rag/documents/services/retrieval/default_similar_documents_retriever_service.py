from __future__ import annotations

from collections.abc import Sequence
from typing import override

from gat.rag.documents.models.document import Document
from gat.rag.documents.services.retrieval.similar_documents_retrieval_service import (
    SimilarDocumentsRetrievalServiceProtocol,
)


class DefaultSimilarDocumentsRetrieverService(SimilarDocumentsRetrievalServiceProtocol):
    @override
    async def retrieve_similar_async(self, query: str) -> Sequence[Document]:
        return await self.repository.read_all({"query": query})
