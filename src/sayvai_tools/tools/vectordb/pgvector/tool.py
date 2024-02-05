from typing import Any

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import PGVector


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
            embedding_function=self.embeddings,
        )

    @classmethod
    def create(cls, embeddings: Any, collection_name: str, connection_string: str) -> cls:
        return cls(embeddings, collection_name, connection_string)

    def _run(
        self,
        query: str,
        k: int = 2,
    ) -> str:
        similar_docs = self.docsearch.similarity_search_with_score(query, k=k)
        return similar_docs

    async def _arun(self, query: str):
        return NotImplementedError("pinecone async not implemented")


class LoadDocs:
    """The PGVector Module will try to create a table with the name of the collection.
    So, make sure that the collection name is unique and the user has the permission to create a table.
    """

    def __init__(
        self, directory, embeddings: Any, collection_name: str, connection_string: str
    ):
        self.directory = directory
        self.embeddings = embeddings
        self.connection_string = connection_string
        self.collection_name = collection_name

    def load_dir(self, directory):
        loader = DirectoryLoader(directory)
        documents = loader.load()
        return documents

    def split_docs(self, chunk_size=1000, chunk_overlap=20):
        documents = self.load_dir(self.directory)
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        docs = text_splitter.split_documents(documents)
        return docs

    def docs_load(self):
        db = PGVector.from_documents(
            embedding=self.embeddings,
            documents=self.split_docs(),
            collection_name=self.collection_name,
            connection_string=self.connection_string,
        )
        return db
