from langchain.vectorstores import Pinecone
from typing import Any


class VectorDB:
    """Tool that queries vector database."""

    name = "vector"
    description = (
        "Useful for when you need to answer questions about the hotel. "
        "Input should be a fully formed question."
    )

    def __init__(self, embeddings: Any, index_name: str, namespace: str):
        self.embeddings = embeddings
        self.index_name = index_name
        self.namespace = namespace
        self.docsearch = Pinecone.from_existing_index(self.index_name, self.embeddings, namespace=self.namespace)

    def _run(
            self,
            query: str,
    ) -> str:
        similar_docs = self.docsearch.similarity_search_with_score(query, k=2)
        return str(similar_docs)

    async def _arun(self, query: str):
        return NotImplementedError("pinecone async not implemented")
