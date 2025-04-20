# OpenAI embeddings model interface
from langchain_openai import OpenAIEmbeddings
from utils.config import OPENAI_API_KEY, EMBEDDING_MODEL

def get_embeddings_model():
    """Returns the OpenAI embeddings model."""
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )