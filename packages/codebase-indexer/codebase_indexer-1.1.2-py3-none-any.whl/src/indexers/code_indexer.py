"""
Code indexer using LangChain, OpenAI, and Pinecone
Implements codebase indexing functionality for Milestone 3
"""
import os
import time
import uuid
import logging
from typing import List, Dict, Any, Optional, Tuple, Iterator
from tqdm import tqdm
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec

from src.utils.config import DEFAULT_INDEX_NAME, CHUNK_SIZE, CHUNK_OVERLAP, PINECONE_API_KEY
from src.utils.pinecone_utils import init_pinecone, create_index_if_not_exists
from src.utils.file_utils import (
    load_documents, 
    chunk_documents, 
    scan_codebase, 
    get_file_language
)
from src.models.embeddings import get_embeddings_model

# Logger
logger = logging.getLogger(__name__)

class CodeIndexer:
    """Class for indexing code files into Pinecone."""
    
    def __init__(self, 
                index_name: str = DEFAULT_INDEX_NAME,
                chunk_size: int = CHUNK_SIZE,
                chunk_overlap: int = CHUNK_OVERLAP):
        """Initialize the code indexer.
        
        Args:
            index_name: Name of the Pinecone index to use.
            chunk_size: Size of code chunks.
            chunk_overlap: Overlap between chunks.
        """
        self.index_name = index_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = get_embeddings_model()
        
        # Initialize Pinecone client
        self.pc = init_pinecone()
        
        # Create index if it doesn't exist and get the Index instance
        self.pinecone_index = create_index_if_not_exists(
            index_name=self.index_name
        )
        
        # Create the LangChain vectorstore wrapper
        self.vectorstore = PineconeVectorStore(
            index=self.pinecone_index,
            embedding=self.embeddings,
            text_key="text"
        )
        
        logger.info(f"Initialized CodeIndexer with index_name={index_name}, "
                   f"chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
    
    def index_codebase(self, 
                      documents: List[Document],
                      batch_size: int = 100,
                      namespace: Optional[str] = None,
                      show_progress: bool = True) -> int:
        """Index a list of documents.
        
        Args:
            documents: List of Document objects to index.
            batch_size: Size of batches for indexing.
            namespace: Namespace to use in Pinecone.
            show_progress: Whether to show a progress bar.
            
        Returns:
            The number of documents indexed.
        """
        logger.info(f"Indexing {len(documents)} documents...")
        
        # Chunk the documents
        chunked_docs = chunk_documents(
            documents,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        # Process the documents in batches to avoid memory issues
        total_chunks = len(chunked_docs)
        indexed_chunks = 0
        
        # Set up progress bar
        pbar = tqdm(total=total_chunks, disable=not show_progress)
        pbar.set_description("Indexing chunks")
        
        # Process in batches
        for i in range(0, total_chunks, batch_size):
            end_idx = min(i + batch_size, total_chunks)
            batch = chunked_docs[i:end_idx]
            
            # Add the batch to the index
            self._add_documents(batch, namespace)
            
            # Update progress
            indexed_chunks += len(batch)
            pbar.update(len(batch))
            
            # Avoid rate limiting
            if end_idx < total_chunks:
                time.sleep(0.25)  # small pause between batches
        
        pbar.close()
        logger.info(f"Successfully indexed {indexed_chunks} chunks")
        
        return indexed_chunks
    
    def _add_documents(self, 
                     documents: List[Document], 
                     namespace: Optional[str] = None) -> List[str]:
        """Add documents to the index.
        
        Args:
            documents: List of Document objects.
            namespace: Namespace to use in Pinecone.
            
        Returns:
            List of IDs of the indexed documents.
        """
        # Generate embeddings for the documents
        texts = [doc.page_content for doc in documents]
        metadatas = [self._process_metadata(doc.metadata) for doc in documents]
        
        # Generate unique IDs for the documents
        ids = [str(uuid.uuid4()) for _ in range(len(documents))]
        
        # Add the documents to the vectorstore
        self.vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids,
            namespace=namespace
        )
        
        return ids
    
    def _process_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Process document metadata to ensure it's compatible with Pinecone.
        
        Args:
            metadata: The document metadata.
            
        Returns:
            Processed metadata compatible with Pinecone.
        """
        # Make a copy of the metadata to avoid modifying the original
        processed = metadata.copy()
        
        # Ensure all values are strings or numbers
        for key, value in processed.items():
            if not isinstance(value, (str, int, float, bool)):
                processed[key] = str(value)
        
        return processed
    
    def index_file(self, 
                  file_path: str,
                  namespace: Optional[str] = None) -> int:
        """Index a single file.
        
        Args:
            file_path: Path to the file to index.
            namespace: Namespace to use in Pinecone.
            
        Returns:
            The number of chunks indexed.
        """
        logger.info(f"Indexing file: {file_path}")
        
        try:
            # Load document
            loader = TextLoader(file_path)
            documents = loader.load()
            
            # Add metadata
            for doc in documents:
                doc.metadata['language'] = get_file_language(file_path)
                doc.metadata['path'] = file_path
                doc.metadata['filename'] = os.path.basename(file_path)
                
            # Index the document
            num_chunks = self.index_codebase(
                documents=documents, 
                namespace=namespace,
                show_progress=False
            )
            
            logger.info(f"Successfully indexed file: {file_path} with {num_chunks} chunks")
            return num_chunks
            
        except Exception as e:
            logger.error(f"Error indexing file {file_path}: {e}")
            return 0
    
    def index_directory(self, 
                       directory_path: str,
                       namespace: Optional[str] = None,
                       extensions: Optional[List[str]] = None,
                       ignore_dirs: Optional[List[str]] = None,
                       ignore_files: Optional[List[str]] = None,
                       show_progress: bool = True) -> int:
        """Index a directory of files.
        
        Args:
            directory_path: Path to the directory to index.
            namespace: Namespace to use in Pinecone.
            extensions: List of file extensions to include.
            ignore_dirs: List of directories to ignore.
            ignore_files: List of files to ignore.
            show_progress: Whether to show a progress bar.
            
        Returns:
            The number of documents indexed.
        """
        logger.info(f"Indexing directory: {directory_path}")
        
        try:
            # Load documents
            documents = load_documents(
                codebase_path=directory_path,
                extensions=extensions,
                ignore_dirs=ignore_dirs,
                ignore_files=ignore_files,
                show_progress=show_progress
            )
            
            # Index the documents
            num_chunks = self.index_codebase(
                documents=documents,
                namespace=namespace,
                show_progress=show_progress
            )
            
            logger.info(f"Successfully indexed directory: {directory_path} with {num_chunks} chunks")
            return num_chunks
            
        except Exception as e:
            logger.error(f"Error indexing directory {directory_path}: {e}")
            return 0
    
    def delete_namespace(self, namespace: str):
        """Delete a namespace from the index.
        
        Args:
            namespace: The namespace to delete.
        """
        logger.info(f"Deleting namespace: {namespace}")
        
        try:
            self.pinecone_index.delete(delete_all=True, namespace=namespace)
            logger.info(f"Successfully deleted namespace: {namespace}")
        except Exception as e:
            logger.error(f"Error deleting namespace {namespace}: {e}")
    
    def delete_index(self):
        """Delete the entire index."""
        logger.info(f"Deleting index: {self.index_name}")
        
        try:
            self.pc.delete_index(self.index_name)
            logger.info(f"Successfully deleted index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error deleting index {self.index_name}: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the index.
        
        Returns:
            Dictionary of index statistics.
        """
        logger.info("Getting index statistics...")
        
        try:
            # Get index stats
            stats = self.pinecone_index.describe_index_stats()
            
            # Format the stats
            formatted_stats = {
                "index_name": self.index_name,
                "dimension": stats.get("dimension"),
                "total_vector_count": stats.get("total_vector_count", 0),
                "namespaces": {}
            }
            
            # Add namespace stats
            namespaces = stats.get("namespaces", {})
            for ns, ns_stats in namespaces.items():
                formatted_stats["namespaces"][ns] = {
                    "vector_count": ns_stats.get("vector_count", 0)
                }
            
            logger.info(f"Successfully got statistics for index: {self.index_name}")
            return formatted_stats
        
        except Exception as e:
            logger.error(f"Error getting statistics for index {self.index_name}: {e}")
            return {"error": str(e)}
    
    def get_namespaces(self) -> List[str]:
        """Get all namespaces in the index.
        
        Returns:
            List of namespaces.
        """
        logger.info("Getting namespaces...")
        
        try:
            # Get index stats
            stats = self.pinecone_index.describe_index_stats()
            
            # Extract namespaces
            namespaces = list(stats.get("namespaces", {}).keys())
            
            logger.info(f"Successfully got namespaces for index: {self.index_name}")
            return namespaces
        
        except Exception as e:
            logger.error(f"Error getting namespaces for index {self.index_name}: {e}")
            return []
    
    def get_sample_vectors(self, namespace: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample vectors from the index.
        
        Args:
            namespace: Namespace to get vectors from. If None, gets from all namespaces.
            limit: Maximum number of vectors to return.
            
        Returns:
            List of vectors with their metadata.
        """
        logger.info(f"Getting sample vectors from namespace: {namespace or 'all'}")
        
        try:
            # Query for random vectors
            # This is a simple way to get random vectors, not truly random
            # For a truly random sample, you'd need to implement a more sophisticated approach
            results = self.vectorstore.similarity_search(
                query="",  # Empty query to get random vectors
                k=limit,
                namespace=namespace
            )
            
            # Format the results
            vectors = []
            for doc in results:
                vectors.append({
                    "text": doc.page_content,
                    "metadata": doc.metadata
                })
            
            logger.info(f"Successfully got {len(vectors)} sample vectors")
            return vectors
        
        except Exception as e:
            logger.error(f"Error getting sample vectors: {e}")
            return []