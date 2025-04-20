"""
Code-aware agent using LangChain, Pinecone, and Claude
To be implemented fully in Milestone 4
"""
import os
import logging
from typing import List, Dict, Any, Optional
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from src.utils.config import DEFAULT_INDEX_NAME
from src.utils.pinecone_utils import init_pinecone
from src.models.embeddings import get_embeddings_model
from src.models.llm import get_llm_model

# Logger
logger = logging.getLogger(__name__)

class CodeAgent:
    """Class for querying code via a RAG system."""
    
    def __init__(self, index_name: str = DEFAULT_INDEX_NAME):
        """Initialize the code agent.
        
        Args:
            index_name: Name of the Pinecone index to use.
        """
        self.index_name = index_name
        self.embeddings = get_embeddings_model()
        self.llm = get_llm_model()
        
        # Initialize Pinecone client
        self.pc = init_pinecone()
        self.vectorstore = None
        
        try:
            # Get the index instance
            pinecone_index = self.pc.Index(self.index_name)
            
            # Create PineconeVectorStore from the index
            self.vectorstore = PineconeVectorStore(
                index=pinecone_index,
                embedding=self.embeddings,
                text_key="text"
            )
            logger.info(f"Initialized vectorstore from index: {self.index_name}")
        except Exception as e:
            logger.warning(f"Failed to initialize vectorstore: {e}")
            logger.warning("Vectorstore will be initialized in the query method if needed")
        
        # Create memory for conversational context
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        logger.info(f"Initialized CodeAgent with index_name={index_name}")
    
    def query(self, 
             query_text: str,
             namespace: Optional[str] = None,
             top_k: int = 5,
             include_sources: bool = True,
             use_mmr: bool = True,
             mmr_diversity: float = 0.3) -> Dict[str, Any]:
        """Query the indexed codebase.
        
        Args:
            query_text: The query string.
            namespace: Namespace to use in Pinecone.
            top_k: Number of documents to retrieve.
            include_sources: Whether to include source documents in the response.
            use_mmr: Whether to use Maximum Marginal Relevance for retrieval.
            mmr_diversity: Diversity of results when using MMR (0-1).
            
        Returns:
            dict: Result containing the response and source documents.
        """
        logger.info(f"Querying codebase with: {query_text}")
        
        if self.vectorstore is None:
            logger.error("Vectorstore not initialized")
            return {
                "query": query_text,
                "result": "Error: Vector store not initialized. Please check that the index exists.",
                "source_documents": []
            }
        
        try:
            # Create a retriever with the specified namespace and number of results
            if use_mmr:
                # Use Maximum Marginal Relevance to get more diverse results
                # This helps avoid redundant code snippets
                retriever = self.vectorstore.as_retriever(
                    search_type="mmr",
                    search_kwargs={
                        "k": top_k * 2,  # Fetch more candidates for MMR filtering
                        "fetch_k": top_k * 3,  # Consider more candidates for diversity
                        "lambda_mult": 1 - mmr_diversity,  # Convert diversity to lambda multiplier
                        "namespace": namespace
                    }
                )
                logger.info(f"Using MMR retrieval with diversity={mmr_diversity}")
            else:
                # Use standard similarity search
                retriever = self.vectorstore.as_retriever(
                    search_kwargs={"k": top_k, "namespace": namespace}
                )
                logger.info("Using standard similarity search")
            
            # Create a RetrievalQA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",  # 'stuff' combines all documents into a single context
                retriever=retriever,
                return_source_documents=include_sources,
                verbose=True
            )
            
            # Set up prompt template for code-specific queries
            from langchain.prompts import PromptTemplate
            
            prompt_template = """You are a code assistant specialized in Python who helps users understand codebases.
Answer the following query based only on the provided code snippets.
If the information is not in the snippets, say so politely.
Where appropriate, include short code examples in your answer.

Based on the query type, format your response accordingly:
- If about code functionality: explain how the code works, what inputs it takes, what outputs it produces, and any side effects
- If about code structure: explain the architecture, class hierarchies, or module organization
- If about a specific feature: explain where and how it's implemented
- If about dependencies: explain which modules depend on each other and how they interact

Some things you can help with:
1. Explaining how specific functions or classes work
2. Describing the architecture of the codebase
3. Finding where certain functionality is implemented
4. Understanding the relationships between different parts of the code
5. Describing API usage patterns

Context code snippets:
{context}

Query: {question}

Answer: """
            
            qa_chain.combine_documents_chain.llm_chain.prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Run the chain
            logger.info("Running QA chain...")
            # Use invoke instead of __call__ to avoid deprecation warnings
            if hasattr(qa_chain, 'invoke'):
                result = qa_chain.invoke({"query": query_text})
            else:
                # Fallback to __call__ if invoke is not available
                result = qa_chain({"query": query_text})
            
            logger.info("Successfully queried codebase")
            return {
                "query": query_text,
                "result": result["result"],
                "source_documents": result["source_documents"] if include_sources else []
            }
            
        except Exception as e:
            logger.error(f"Error querying codebase: {e}")
            logger.exception("Exception details:")
            return {
                "query": query_text,
                "result": f"Error querying codebase: {str(e)}",
                "source_documents": []
            }
    
    def chat(self, 
            query_text: str,
            namespace: Optional[str] = None,
            top_k: int = 5,
            use_mmr: bool = True,
            mmr_diversity: float = 0.3) -> Dict[str, Any]:
        """Chat with the agent with conversation history.
        
        Args:
            query_text: The query string.
            namespace: Namespace to use in Pinecone.
            top_k: Number of documents to retrieve.
            use_mmr: Whether to use Maximum Marginal Relevance for retrieval.
            mmr_diversity: Diversity of results when using MMR (0-1).
            
        Returns:
            dict: Result containing the response and source documents.
        """
        logger.info(f"Chatting with agent: {query_text}")
        
        if self.vectorstore is None:
            logger.error("Vectorstore not initialized")
            return {
                "query": query_text,
                "result": "Error: Vector store not initialized. Please check that the index exists.",
                "source_documents": []
            }
        
        try:
            # Create a retriever with the specified namespace and number of results
            if use_mmr:
                # Use Maximum Marginal Relevance for more diverse results
                retriever = self.vectorstore.as_retriever(
                    search_type="mmr",
                    search_kwargs={
                        "k": top_k * 2,  # Fetch more candidates for MMR filtering
                        "fetch_k": top_k * 3,  # Consider more candidates for diversity
                        "lambda_mult": 1 - mmr_diversity,  # Convert diversity to lambda multiplier
                        "namespace": namespace
                    }
                )
                logger.info(f"Using MMR retrieval with diversity={mmr_diversity}")
            else:
                # Use standard similarity search
                retriever = self.vectorstore.as_retriever(
                    search_kwargs={"k": top_k, "namespace": namespace}
                )
                logger.info("Using standard similarity search")
            
            # Create a ConversationalRetrievalChain - note: API changed in newer versions
            try:
                # First try with current parameters (newer LangChain versions)
                chat_chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    return_source_documents=True,
                    verbose=True
                )
            except Exception as chain_error:
                logger.warning(f"Error creating ConversationalRetrievalChain with current params: {chain_error}")
                # Try with older-style parameters
                chat_chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    return_source_documents=True,
                    verbose=True,
                    memory=self.memory
                )
            
            # Set up a better prompt for the conversation
            from langchain.prompts import PromptTemplate
            
            # First try to use the system prompt approach for newer LangChain versions
            system_prompt = """You are a code assistant that helps users understand codebases.
You maintain context across the conversation.
Answer questions based on the provided code snippets.
If the information is not in the snippets, say so politely.
Where appropriate, include code examples in your answer.
Be concise but thorough."""
            
            try:
                # Try to add system prompt to the chain if applicable
                if hasattr(chat_chain, 'combine_docs_chain') and hasattr(chat_chain.combine_docs_chain, 'llm_chain'):
                    current_prompt = chat_chain.combine_docs_chain.llm_chain.prompt
                    if hasattr(current_prompt, 'messages'):
                        # Try to add the system prompt at the beginning
                        try:
                            from langchain_core.messages import SystemMessage
                            current_prompt.messages[0] = SystemMessage(content=system_prompt)
                            logger.info("Successfully set system prompt for conversation")
                        except Exception as e:
                            logger.warning(f"Could not set system message: {e}")
            except Exception as e:
                logger.warning(f"Error setting system prompt: {e}")
                
            # As a fallback, try to update the prompt template
            try:
                condense_prompt_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question that captures all relevant context from the conversation.

Chat History:
{chat_history}

Follow Up Input: {question}

Standalone Question:"""
                
                qa_prompt_template = """You are a code assistant that helps users understand codebases.
You maintain context across the conversation.
Answer the following question based on the provided code snippets.
If the information is not in the snippets, say so politely.
Where appropriate, include code examples in your answer.
Be concise but thorough.

Some things you can help with:
1. Explaining how specific functions or classes work
2. Describing the architecture of the codebase
3. Finding where certain functionality is implemented
4. Understanding the relationships between different parts of the code
5. Suggesting improvements or identifying potential issues

Context code snippets:
{context}

Question: {question}

Answer:"""
                
                # Try to set the prompt templates if the appropriate attributes exist
                if hasattr(chat_chain, 'question_generator') and hasattr(chat_chain.question_generator, 'prompt'):
                    chat_chain.question_generator.prompt = PromptTemplate.from_template(condense_prompt_template)
                    
                if hasattr(chat_chain, 'combine_docs_chain') and hasattr(chat_chain.combine_docs_chain, 'llm_chain') and hasattr(chat_chain.combine_docs_chain.llm_chain, 'prompt'):
                    chat_chain.combine_docs_chain.llm_chain.prompt = PromptTemplate.from_template(qa_prompt_template)
                    
                logger.info("Set prompt templates for conversation")
            except Exception as e:
                logger.warning(f"Error setting prompt templates: {e}")
            
            # Run the chain
            logger.info("Running conversational chain...")
            # Include empty chat_history if needed
            inputs = {"question": query_text}
            
            # Check if this chain expects a chat_history
            if hasattr(chat_chain, 'input_keys') and 'chat_history' in chat_chain.input_keys:
                inputs["chat_history"] = []
                
            # Use invoke instead of __call__ to avoid deprecation warnings
            if hasattr(chat_chain, 'invoke'):
                result = chat_chain.invoke(inputs)
            else:
                # Fallback to __call__ if invoke is not available
                result = chat_chain(inputs)
            
            logger.info("Successfully chatted with codebase")
            return {
                "query": query_text,
                "result": result["answer"],
                "source_documents": result.get("source_documents", [])
            }
            
        except Exception as e:
            logger.error(f"Error chatting with codebase: {e}")
            logger.exception("Exception details:")
            return {
                "query": query_text,
                "result": f"Error chatting with codebase: {str(e)}",
                "source_documents": []
            }
    
    def get_related_code(self, 
                       query_text: str,
                       namespace: Optional[str] = None,
                       top_k: int = 10,
                       use_mmr: bool = True,
                       mmr_diversity: float = 0.3) -> List[Dict[str, Any]]:
        """Get code snippets related to a query without generating an answer.
        
        Args:
            query_text: The query string.
            namespace: Namespace to use in Pinecone.
            top_k: Number of documents to retrieve.
            use_mmr: Whether to use Maximum Marginal Relevance for retrieval.
            mmr_diversity: Diversity of results when using MMR (0-1).
            
        Returns:
            List of dictionaries containing the code snippets and metadata.
        """
        logger.info(f"Getting code related to: {query_text}")
        
        if self.vectorstore is None:
            logger.error("Vectorstore not initialized")
            return []
        
        try:
            # Perform a retrieval search
            if use_mmr:
                # Use Maximum Marginal Relevance for more diverse results
                docs = self.vectorstore.max_marginal_relevance_search(
                    query=query_text,
                    k=top_k,
                    fetch_k=top_k * 3,  # Fetch more candidates for MMR
                    lambda_mult=1 - mmr_diversity,  # Convert diversity to lambda multiplier
                    namespace=namespace
                )
                logger.info(f"Used MMR search with diversity={mmr_diversity}")
            else:
                # Standard similarity search
                docs = self.vectorstore.similarity_search(
                    query=query_text, 
                    k=top_k,
                    namespace=namespace
                )
                logger.info("Used standard similarity search")
            
            # Format the results
            results = []
            for doc in docs:
                # Extract file path and line information if available
                source_file = doc.metadata.get('source', doc.metadata.get('path', 'Unknown file'))
                language = doc.metadata.get('language', 'unknown')
                
                # Format the result
                result = {
                    'code': doc.page_content,
                    'file': source_file,
                    'language': language,
                    'metadata': doc.metadata
                }
                results.append(result)
            
            logger.info(f"Found {len(results)} code snippets related to the query")
            return results
            
        except Exception as e:
            logger.error(f"Error getting related code: {e}")
            logger.exception("Exception details:")
            return []