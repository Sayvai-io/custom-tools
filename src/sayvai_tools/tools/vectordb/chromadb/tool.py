from typing import Any

from langchain.document_loaders import DirectoryLoader
# from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


class ChromaDB:
    """Tool that queries vector database."""

    name = "chroma"
    description = (
        "Useful for when you need to answer any questions"
        "Input should be a fully formed question."
    )

    def __init__(self, embeddings: Any, persist_directory: str):
        self.embeddings = embeddings
        self.persist_directory = persist_directory
        self.docsearch = Chroma(
            persist_directory=self.persist_directory, embedding_function=self.embeddings
        )

    @classmethod
    def create(cls, **kwargs) -> "ChromaDB":
        return cls(
            embeddings=kwargs["embeddings"],
            persist_directory=kwargs["persist_directory"],
        )

    def _run(
        self,
        query: str,
    ) -> str:
        similar_docs = self.docsearch.similarity_search(query)
        return str(similar_docs)

    async def _arun(self, query: str):
        return NotImplementedError("pinecone async not implemented")


class LoadDocs:
    """Used to load the document into the database"""

    def __init__(self, embeddings, directory, persist_directory):
        self.directory = directory
        self.embeddings = embeddings
        self.persist_directory = persist_directory

    def load_dir(self, directory):
        loader = DirectoryLoader(directory)
        documents = loader.load()
        return documents

    def split_docs(self, chunk_size=1000, chunk_overlap=20):
        documents = self.load_dir(self.directory)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        docs = text_splitter.split_documents(documents)
        return docs

    def docs_load(self):
        index = Chroma.from_documents(
            self.split_docs(), self.embeddings, persist_directory=self.persist_directory
        )
        index.persist()
        return index
