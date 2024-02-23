import os
from typing import Any

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone


class PineconeDB:
    def __init__(self, embeddings: OpenAIEmbeddings | Any, index_name: str, **kwargs):
        self.pinecone = Pinecone(
            pinecone_api_key=kwargs.get(
                "pinecone_api_key", os.environ.get("PINECONE_API_KEY")
            ),
            index_name=index_name,
            embedding=embeddings,
        )

    def _run(self, query: str, k: int = 3):
        return self.pinecone.similarity_search(query=query, k=k)[1:]
