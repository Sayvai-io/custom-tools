# rag template for pinecone
from langchain_openai import OpenAIEmbeddings
from rich import print as rprint

from sayvai_tools.utils.vectorstore.pineconedb import PineconeDB

pinecone_db = PineconeDB(  # type: ignore
    embeddings=OpenAIEmbeddings(),
    index_name="rag-pinecone",
    pinecone_api_key="your_pinecone_api_key",
)

response = pinecone_db._run(query="What is the capital of France?")
rprint(response)
