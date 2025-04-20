import os
from dotenv import load_dotenv

# Load environment variables from .env file (simple approach)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

# API configuration - use os.environ to directly access environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")

# Default index name
DEFAULT_INDEX_NAME = "codebase-index"

# Embedding configuration
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI embedding model

# LLM configuration
LLM_MODEL = os.environ.get("LLM_MODEL", "claude-3-haiku-20240307")  # Claude 3.5 Haiku
# Alternative Claude models if needed:
# "claude-3-haiku-20240307" (3.5 Haiku)
# "claude-3-sonnet-20240229" 
# "claude-3-opus-20240229"
# "claude-3-haiku-20231218"

# Chunking configuration
CHUNK_SIZE = 800  # Larger chunk size to capture more context
CHUNK_OVERLAP = 150  # More overlap to maintain context between chunks

# Retrieval configuration
DEFAULT_TOP_K = 5  # Default number of documents to retrieve
USE_MMR = True  # Use Maximum Marginal Relevance by default
MMR_DIVERSITY = 0.3  # Default diversity parameter for MMR (0-1)

def validate_api_keys(skip_validation=False):
    """Simple validation that checks if API keys are present.
    
    Args:
        skip_validation: If True, don't raise errors for missing keys.
                         This is useful for commands like 'configure'.
    
    Returns:
        list: List of missing API keys
    """
    missing_keys = []
    
    if not OPENAI_API_KEY:
        missing_keys.append("OPENAI_API_KEY")
    if not ANTHROPIC_API_KEY:
        missing_keys.append("ANTHROPIC_API_KEY")
    if not PINECONE_API_KEY:
        missing_keys.append("PINECONE_API_KEY")
    
    # Only raise an error if we're not skipping validation and there are missing keys
    if missing_keys and not skip_validation:
        raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}. "
                        f"Please run 'codebase-indexer configure' to set them.")
    
    return missing_keys