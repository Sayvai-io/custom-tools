from typing import Any, Optional
from sayvai_tools.utils import deprecated
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone


@deprecated("Use sayvai_tools.tools.PineconeDB instead")
class PineconeDB:
    """Tool that queries vector database."""

    name = "pinecone"
    description = (
        "Useful for when you need to answer any questions"
        "Input should be a fully formed question."
    )

    def __init__(self, embeddings: Any, index_name: str, namespace: str):
        self.embeddings = embeddings
        self.index_name = index_name
        self.namespace = namespace
        self.docsearch = Pinecone.from_existing_index(
            self.index_name, self.embeddings, namespace=self.namespace
        )

    @classmethod
    def create(cls, **kwargs) -> "PineconeDB":
        return cls(
            embeddings=kwargs["embeddings"],
            index_name=kwargs["index_name"],
            namespace=kwargs["namespace"],
        )

    def _run(
        self,
        query: str,
    ) -> str:
        similar_docs = self.docsearch.similarity_search_with_score(query, k=2)
        return str(similar_docs)

    async def _arun(self, query: str):
        return NotImplementedError("pinecone async not implemented")


class LoadDocs:
    def __init__(
        self, embeddings, directory, index_name, namespace: Optional[str] = None
    ):
        self.directory = directory
        self.embeddings = embeddings
        self.index_name = index_name
        self.namespace = namespace

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
        index = Pinecone.from_documents(
            self.split_docs(),
            self.embeddings,
            index_name=self.index_name,
            namespace=self.namespace,
        )
        return index
