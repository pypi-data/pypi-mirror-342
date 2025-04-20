import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Default index name
DEFAULT_INDEX_NAME = "codebase-index"

# Embedding configuration
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI embedding model

# LLM configuration
LLM_MODEL = "claude-3-haiku-20240307"  # Claude 3.5 Haiku
# Alternative Claude models if needed:
# "claude-3-haiku-20240307" (3.5 Haiku)
# "claude-3-sonnet-20240229" 
# "claude-3-opus-20240229"
# "claude-3-haiku-20231218"

# Chunking configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def validate_api_keys():
    """Validate that all required API keys are present."""
    missing_keys = []
    
    if not OPENAI_API_KEY:
        missing_keys.append("OPENAI_API_KEY")
    if not ANTHROPIC_API_KEY:
        missing_keys.append("ANTHROPIC_API_KEY")
    if not PINECONE_API_KEY:
        missing_keys.append("PINECONE_API_KEY")
    
    if missing_keys:
        raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}. "
                        f"Please add them to your .env file.")