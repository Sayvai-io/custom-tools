from typing import Any
from langchain.vectorstores.pgvector import PGVector

class PGVectorDB:
    """Tool that queries vector database."""

    name = "pgvector"
    description = (
        "Useful for when you need to answer any questions"
        "Input should be a fully formed question."
    )

    def __init__(self, embeddings: Any, collection_name: str, connection_string: str):
        self.embeddings = embeddings
        self.connection_string = connection_string
        self.collection_name = collection_name
        self.docsearch = PGVector(
                            collection_name=self.collection_name,
                            connection_string=self.connection_string,
                            embedding_function=self.embeddings
                        ) 

    def _run(
            self,
            query: str,
            k: int = 2,
    ) -> str:
        similar_docs = self.docsearch.similarity_search_with_score(query, k=k)
        return similar_docs

    async def _arun(self, query: str):
        return NotImplementedError("pinecone async not implemented")