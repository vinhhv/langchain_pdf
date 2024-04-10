import os
import pinecone
from app.chat.embeddings.openai import embeddings
from langchain.vectorstores import Pinecone

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV_NAME")
)

vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)
