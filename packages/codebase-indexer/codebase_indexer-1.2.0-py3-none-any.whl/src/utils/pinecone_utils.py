"""
Utilities for working with Pinecone
"""
import os
import logging
from typing import Dict, List, Optional, Any
from pinecone import Pinecone, Index, ServerlessSpec

from src.utils.config import PINECONE_API_KEY

# Logger
logger = logging.getLogger(__name__)

def init_pinecone():
    """Initialize Pinecone client.
    
    Returns:
        Pinecone client instance
    """
    try:
        # Initialize Pinecone client
        pc = Pinecone(api_key=PINECONE_API_KEY)
        logger.info("Initialized Pinecone client")
        return pc
    except Exception as e:
        logger.error(f"Error initializing Pinecone client: {e}")
        raise

def create_index_if_not_exists(index_name: str, dimension: int = 1536, metric: str = "cosine"):
    """Create a Pinecone index if it doesn't exist.
    
    Args:
        index_name: Name of the index to create.
        dimension: Dimension of the embedding vectors (1536 for OpenAI ada-002).
        metric: Similarity metric to use (cosine, dotproduct, or euclidean).
    
    Returns:
        Index: Pinecone index
    """
    try:
        # Initialize Pinecone client
        pc = init_pinecone()
        
        # Check if index already exists
        if index_name in pc.list_indexes().names():
            logger.info(f"Using existing Pinecone index: {index_name}")
            return pc.Index(index_name)
        
        # Create serverless index
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        logger.info(f"Created new Pinecone index: {index_name}")
        
        # Return the index
        return pc.Index(index_name)
    
    except Exception as e:
        logger.error(f"Error creating Pinecone index: {e}")
        raise

def delete_index(index_name: str):
    """Delete a Pinecone index.
    
    Args:
        index_name: Name of the index to delete.
    """
    try:
        # Initialize Pinecone client
        pc = init_pinecone()
        
        # Check if index exists
        if index_name not in pc.list_indexes().names():
            logger.warning(f"Index {index_name} does not exist")
            return
        
        # Delete index
        pc.delete_index(index_name)
        logger.info(f"Deleted Pinecone index: {index_name}")
    
    except Exception as e:
        logger.error(f"Error deleting Pinecone index: {e}")
        raise

def list_indexes() -> List[str]:
    """List all Pinecone indexes.
    
    Returns:
        List of index names.
    """
    try:
        # Initialize Pinecone client
        pc = init_pinecone()
        
        # List indexes
        indexes = pc.list_indexes().names()
        logger.info(f"Found {len(indexes)} Pinecone indexes")
        return indexes
    
    except Exception as e:
        logger.error(f"Error listing Pinecone indexes: {e}")
        return []

def get_index_stats(index_name: str) -> Dict[str, Any]:
    """Get statistics for a Pinecone index.
    
    Args:
        index_name: Name of the index to get stats for.
        
    Returns:
        Dictionary containing index statistics.
    """
    try:
        # Initialize Pinecone client
        pc = init_pinecone()
        
        # Check if index exists
        if index_name not in pc.list_indexes().names():
            logger.warning(f"Index {index_name} does not exist")
            return {"error": f"Index {index_name} does not exist"}
        
        # Get index
        index = pc.Index(index_name)
        
        # Get index stats
        stats = index.describe_index_stats()
        logger.info(f"Got stats for Pinecone index: {index_name}")
        return stats
    
    except Exception as e:
        logger.error(f"Error getting stats for Pinecone index: {e}")
        return {"error": str(e)}

def delete_vectors(index_name: str, ids: List[str], namespace: Optional[str] = None):
    """Delete vectors from a Pinecone index.
    
    Args:
        index_name: Name of the index to delete vectors from.
        ids: List of vector IDs to delete.
        namespace: Namespace to delete vectors from.
    """
    try:
        # Initialize Pinecone client
        pc = init_pinecone()
        
        # Check if index exists
        if index_name not in pc.list_indexes().names():
            logger.warning(f"Index {index_name} does not exist")
            return
        
        # Get index
        index = pc.Index(index_name)
        
        # Delete vectors
        index.delete(ids=ids, namespace=namespace)
        logger.info(f"Deleted {len(ids)} vectors from Pinecone index: {index_name}")
    
    except Exception as e:
        logger.error(f"Error deleting vectors from Pinecone index: {e}")
        raise