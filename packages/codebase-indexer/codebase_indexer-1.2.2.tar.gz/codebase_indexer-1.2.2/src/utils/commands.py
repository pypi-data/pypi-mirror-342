"""
Command handling utilities for the CLI
"""
import os
import sys
import json
import logging
import argparse
from typing import List, Dict, Any, Optional, Callable

from src.utils.config import validate_api_keys
from src.utils.logger import setup_logger
from src.utils.file_utils import load_documents, chunk_documents, scan_codebase
from src.utils.pinecone_utils import create_index_if_not_exists, init_pinecone, delete_index, list_indexes, get_index_stats
from src.utils.project_metadata import extract_project_metadata
from src.utils.code_analysis import analyze_code
from src.indexers.code_indexer import CodeIndexer
from src.agents.code_agent import CodeAgent

# Logger
logger = logging.getLogger(__name__)

def setup_arg_parser():
    """Set up the command-line argument parser.
    
    Returns:
        ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Command-line tool for indexing and querying large codebases",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Index command
    index_parser = subparsers.add_parser("index", help="Index a codebase")
    index_parser.add_argument("--path", required=True, help="Path to the codebase directory")
    index_parser.add_argument("--index-name", default="codebase-index", help="Pinecone index name")
    index_parser.add_argument("--chunk-size", type=int, default=500, help="Size of code chunks (recommended: 300-800)")
    index_parser.add_argument("--chunk-overlap", type=int, default=100, help="Overlap between chunks (recommended: 50-150)")
    index_parser.add_argument("--force", action="store_true", help="Force reindexing if index already exists")
    index_parser.add_argument("--extensions", help="Comma-separated list of file extensions to index (e.g., py,js,java)")
    index_parser.add_argument("--namespace", help="Namespace to use in Pinecone for this codebase")
    index_parser.add_argument("--batch-size", type=int, default=300, help="Batch size for indexing (larger batches = faster)")
    index_parser.add_argument("--parallel", type=int, default=2, help="Number of batches to process in parallel")
    index_parser.add_argument("--concurrency", type=int, default=10, help="Maximum concurrent embedding requests per batch")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List files in a codebase")
    list_parser.add_argument("--path", required=True, help="Path to the codebase directory")
    list_parser.add_argument("--extensions", help="Comma-separated list of file extensions to include (e.g., py,js,java)")
    list_parser.add_argument("--count", action="store_true", help="Show file count by extension")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a codebase")
    analyze_parser.add_argument("--path", required=True, help="Path to the codebase directory")
    analyze_parser.add_argument("--output", help="Path to output file for analysis results")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan a codebase and output metadata")
    scan_parser.add_argument("--path", required=True, help="Path to the codebase directory")
    scan_parser.add_argument("--extensions", help="Comma-separated list of file extensions to include (e.g., py,js,java)")
    scan_parser.add_argument("--output", help="Path to output file for scan results")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an index")
    delete_parser.add_argument("--index-name", required=True, help="Pinecone index name to delete")
    delete_parser.add_argument("--namespace", help="Only delete a specific namespace instead of the entire index")
    delete_parser.add_argument("--confirm", action="store_true", help="Confirm deletion without prompting")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics about an index")
    stats_parser.add_argument("--index-name", required=True, help="Pinecone index name")
    stats_parser.add_argument("--json", action="store_true", help="Output statistics in JSON format")
    
    # List indexes command
    list_indexes_parser = subparsers.add_parser("list-indexes", help="List all indexes")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the indexed codebase")
    query_parser.add_argument("--query", required=True, help="Query string")
    query_parser.add_argument("--index-name", default="codebase-index", help="Pinecone index name")
    query_parser.add_argument("--namespace", help="Namespace to query in Pinecone")
    query_parser.add_argument("--limit", type=int, default=5, help="Maximum number of results to return")
    query_parser.add_argument("--no-mmr", dest="use_mmr", action="store_false", help="Disable Maximum Marginal Relevance retrieval")
    query_parser.add_argument("--diversity", type=float, default=0.3, help="Diversity parameter for MMR (0-1)")
    query_parser.set_defaults(use_mmr=True)
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with the codebase using conversation history")
    chat_parser.add_argument("--query", required=True, help="Query string")
    chat_parser.add_argument("--index-name", default="codebase-index", help="Pinecone index name")
    chat_parser.add_argument("--namespace", help="Namespace to query in Pinecone")
    chat_parser.add_argument("--limit", type=int, default=5, help="Maximum number of results to return")
    chat_parser.add_argument("--no-mmr", dest="use_mmr", action="store_false", help="Disable Maximum Marginal Relevance retrieval")
    chat_parser.add_argument("--diversity", type=float, default=0.3, help="Diversity parameter for MMR (0-1)")
    chat_parser.set_defaults(use_mmr=True)
    
    # Get related code command
    related_parser = subparsers.add_parser("related", help="Get code snippets related to a query")
    related_parser.add_argument("--query", required=True, help="Query string")
    related_parser.add_argument("--index-name", default="codebase-index", help="Pinecone index name")
    related_parser.add_argument("--namespace", help="Namespace to query in Pinecone")
    related_parser.add_argument("--limit", type=int, default=10, help="Maximum number of results to return")
    related_parser.add_argument("--no-mmr", dest="use_mmr", action="store_false", help="Disable Maximum Marginal Relevance retrieval")
    related_parser.add_argument("--diversity", type=float, default=0.3, help="Diversity parameter for MMR (0-1)")
    related_parser.set_defaults(use_mmr=True)
    
    # Configure command
    configure_parser = subparsers.add_parser("configure", help="Configure API keys and settings")
    configure_parser.add_argument("--openai", help="OpenAI API key")
    configure_parser.add_argument("--anthropic", help="Anthropic API key")
    configure_parser.add_argument("--pinecone", help="Pinecone API key")
    configure_parser.add_argument("--model", help="Claude model name (e.g., claude-3-haiku-20240307)")
    configure_parser.add_argument("--non-interactive", action="store_true", help="Don't prompt for missing values")
    
    # Common options
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    return parser

def handle_index_command(args):
    """Handle the 'index' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Indexing codebase at {args.path} to index {args.index_name}")
    
    # Validate path
    if not os.path.exists(args.path):
        logger.error(f"Path does not exist: {args.path}")
        return 1
    
    if not os.path.isdir(args.path):
        logger.error(f"Path is not a directory: {args.path}")
        return 1
    
    try:
        # Initialize Pinecone
        logger.info("Initializing Pinecone...")
        init_pinecone()
        
        # Check if namespace should be automatically set
        namespace = args.namespace
        if namespace is None:
            # Use directory name as namespace
            namespace = os.path.basename(os.path.abspath(args.path))
            logger.info(f"Using directory name as namespace: {namespace}")
        
        # Create index if it doesn't exist
        create_index_if_not_exists(args.index_name)
        
        # Parse extensions
        extensions = None
        if args.extensions:
            extensions = args.extensions.split(',')
        
        # Create Code Indexer instance
        indexer = CodeIndexer(
            index_name=args.index_name,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        
        # Index the directory with parallel processing
        num_chunks = indexer.index_directory(
            directory_path=args.path,
            namespace=namespace,
            extensions=extensions,
            show_progress=True,
            batch_size=args.batch_size,
            max_concurrent_requests=args.concurrency,
            parallel_batches=args.parallel
        )
        
        logger.info(f"Successfully indexed codebase at {args.path} with {num_chunks} chunks")
        print(f"Successfully indexed {num_chunks} chunks from {args.path} to index {args.index_name} in namespace {namespace}")
        return 0
    
    except Exception as e:
        logger.error(f"Error indexing codebase: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        print(f"Error indexing codebase: {e}")
        return 1

def handle_list_command(args):
    """Handle the 'list' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Listing files in codebase at {args.path}")
    
    # Validate path
    if not os.path.exists(args.path):
        logger.error(f"Path does not exist: {args.path}")
        return 1
    
    if not os.path.isdir(args.path):
        logger.error(f"Path is not a directory: {args.path}")
        return 1
    
    try:
        # Parse extensions filter
        extensions = None
        if args.extensions:
            extensions = [f".{ext.lstrip('.')}" for ext in args.extensions.split(',')]
        
        # Count files by extension
        if args.count:
            extension_counts = {}
            total_files = 0
            
            for root, dirs, files in os.walk(args.path):
                for file in files:
                    # Skip hidden files
                    if file.startswith('.'):
                        continue
                    
                    _, ext = os.path.splitext(file)
                    if extensions and ext not in extensions:
                        continue
                    
                    extension_counts[ext] = extension_counts.get(ext, 0) + 1
                    total_files += 1
            
            # Print results
            print(f"Found {total_files} files in {args.path}")
            for ext, count in sorted(extension_counts.items(), key=lambda x: x[1], reverse=True):
                if ext:
                    print(f"{ext}: {count} files")
                else:
                    print(f"No extension: {count} files")
        
        # List files
        else:
            file_count = 0
            for root, dirs, files in os.walk(args.path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    # Skip hidden files
                    if file.startswith('.'):
                        continue
                    
                    _, ext = os.path.splitext(file)
                    if extensions and ext not in extensions:
                        continue
                    
                    rel_path = os.path.relpath(os.path.join(root, file), args.path)
                    print(rel_path)
                    file_count += 1
            
            logger.info(f"Found {file_count} files")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        return 1

def handle_analyze_command(args):
    """Handle the 'analyze' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Analyzing codebase at {args.path}")
    
    # Validate path
    if not os.path.exists(args.path):
        logger.error(f"Path does not exist: {args.path}")
        return 1
    
    if not os.path.isdir(args.path):
        logger.error(f"Path is not a directory: {args.path}")
        return 1
    
    try:
        # Extract project metadata
        metadata = extract_project_metadata(args.path)
        
        # Print metadata
        print("Project Analysis:")
        print(f"Path: {metadata['path']}")
        print(f"Language: {metadata['language']}")
        print(f"Type: {metadata['type']}")
        
        if 'name' in metadata:
            print(f"Name: {metadata['name']}")
        
        if 'version' in metadata:
            print(f"Version: {metadata['version']}")
        
        print("\nProject Files:")
        for filename in metadata['project_files']:
            print(f"- {filename}")
        
        # Write to output file if specified
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"\nAnalysis saved to {args.output}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error analyzing codebase: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        return 1

def handle_scan_command(args):
    """Handle the 'scan' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Scanning codebase at {args.path}")
    
    # Validate path
    if not os.path.exists(args.path):
        logger.error(f"Path does not exist: {args.path}")
        return 1
    
    if not os.path.isdir(args.path):
        logger.error(f"Path is not a directory: {args.path}")
        return 1
    
    try:
        # Parse extensions filter
        extensions = None
        if args.extensions:
            extensions = [f"*.{ext.lstrip('.')}" for ext in args.extensions.split(',')]
        
        # Scan codebase
        files_metadata = scan_codebase(args.path, extensions)
        
        # Print summary
        print(f"Scanned {len(files_metadata)} files in {args.path}")
        
        # Group files by language
        languages = {}
        for file in files_metadata:
            lang = file['language']
            languages[lang] = languages.get(lang, 0) + 1
        
        print("\nLanguage Breakdown:")
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            print(f"- {lang}: {count} files")
        
        # Write to output file if specified
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(files_metadata, f, indent=2)
            print(f"\nScan results saved to {args.output}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error scanning codebase: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        return 1

def handle_delete_command(args):
    """Handle the 'delete' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    
    if args.namespace:
        logger.info(f"Deleting namespace {args.namespace} from index {args.index_name}")
    else:
        logger.info(f"Deleting index {args.index_name}")
    
    try:
        # Initialize Pinecone
        logger.info("Initializing Pinecone...")
        init_pinecone()
        
        # Confirm deletion
        if not args.confirm:
            if args.namespace:
                confirmation = input(f"Are you sure you want to delete the namespace '{args.namespace}' from index '{args.index_name}'? (y/N): ")
            else:
                confirmation = input(f"Are you sure you want to delete the index '{args.index_name}'? (y/N): ")
                
            if confirmation.lower() not in ['y', 'yes']:
                logger.info("Operation cancelled by user")
                print("Operation cancelled")
                return 0
        
        # Create Code Indexer instance
        indexer = CodeIndexer(index_name=args.index_name)
        
        # Delete namespace or index
        if args.namespace:
            indexer.delete_namespace(args.namespace)
            print(f"Successfully deleted namespace {args.namespace} from index {args.index_name}")
        else:
            indexer.delete_index()
            print(f"Successfully deleted index {args.index_name}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error deleting index: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        print(f"Error deleting index: {e}")
        return 1

def handle_stats_command(args):
    """Handle the 'stats' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Getting statistics for index {args.index_name}")
    
    try:
        # Initialize Pinecone
        logger.info("Initializing Pinecone...")
        init_pinecone()
        
        # Create Code Indexer instance
        indexer = CodeIndexer(index_name=args.index_name)
        
        # Get statistics
        stats = indexer.get_stats()
        
        # Output statistics in JSON format
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            # Print statistics in a human-readable format
            print(f"Statistics for index {args.index_name}:")
            print(f"Dimension: {stats['dimension']}")
            print(f"Total Vector Count: {stats['total_vector_count']}")
            
            if stats["namespaces"]:
                print("\nNamespaces:")
                for ns, ns_stats in stats["namespaces"].items():
                    print(f"- {ns}: {ns_stats['vector_count']} vectors")
            else:
                print("\nNo namespaces found")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        print(f"Error getting statistics: {e}")
        return 1

def handle_list_indexes_command(args):
    """Handle the 'list-indexes' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info("Listing Pinecone indexes")
    
    try:
        # Initialize Pinecone
        logger.info("Initializing Pinecone...")
        init_pinecone()
        
        # List indexes
        indexes = list_indexes()
        
        if indexes:
            print("Pinecone Indexes:")
            for idx in indexes:
                # Get stats for each index
                stats = get_index_stats(idx)
                if "total_vector_count" in stats:
                    print(f"- {idx}: {stats['total_vector_count']} vectors")
                else:
                    print(f"- {idx}")
        else:
            print("No Pinecone indexes found")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error listing indexes: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        print(f"Error listing indexes: {e}")
        return 1

def handle_query_command(args):
    """Handle the 'query' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Querying index {args.index_name} with: {args.query}")
    
    try:
        # Initialize Pinecone
        logger.info("Initializing Pinecone...")
        init_pinecone()
        
        # Create Code Agent instance
        agent = CodeAgent(index_name=args.index_name)
        
        # Query the agent
        logger.info("Querying the agent...")
        print(f"Query: {args.query}")
        
        try:
            # Execute the query
            result = agent.query(
                query_text=args.query,
                namespace=args.namespace,
                top_k=args.limit,
                include_sources=True,
                use_mmr=args.use_mmr,
                mmr_diversity=args.diversity
            )
            
            # Print the result
            print("\nAnswer:")
            print(result["result"])
            
            # Print source documents if available
            if result.get("source_documents"):
                print("\nSources:")
                for i, doc in enumerate(result["source_documents"]):
                    print(f"\n--- Source {i+1} ---")
                    print(f"File: {doc.metadata.get('source', doc.metadata.get('path', 'Unknown'))}")
                    print(f"Language: {doc.metadata.get('language', 'unknown')}")
                    print(f"Content: {doc.page_content[:150]}..." if len(doc.page_content) > 150 else f"Content: {doc.page_content}")
        
        except Exception as query_error:
            logger.error(f"Error during LLM query: {query_error}")
            print("\nError occurred during LLM processing. Falling back to showing relevant code snippets...\n")
            
            # Fallback to just showing code snippets
            code_snippets = agent.get_related_code(
                query_text=args.query,
                namespace=args.namespace,
                top_k=args.limit
            )
            
            if code_snippets:
                print(f"Found {len(code_snippets)} code snippets related to your query:")
                for i, snippet in enumerate(code_snippets):
                    print(f"\n--- Snippet {i+1} ---")
                    print(f"File: {snippet['file']}")
                    print(f"Language: {snippet['language']}")
                    print(f"Code:")
                    print(snippet['code'][:200] + "..." if len(snippet['code']) > 200 else snippet['code'])
            else:
                print("No relevant code snippets found.")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error querying codebase: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        print(f"Error querying codebase: {e}")
        return 1

def handle_chat_command(args):
    """Handle the 'chat' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Chatting with index {args.index_name} with: {args.query}")
    
    try:
        # Initialize Pinecone
        logger.info("Initializing Pinecone...")
        init_pinecone()
        
        # Create Code Agent instance
        agent = CodeAgent(index_name=args.index_name)
        
        # Query the agent
        logger.info("Chatting with the agent...")
        print(f"Query: {args.query}")
        
        try:
            # Execute the chat query
            result = agent.chat(
                query_text=args.query,
                namespace=args.namespace,
                top_k=args.limit,
                use_mmr=args.use_mmr,
                mmr_diversity=args.diversity
            )
            
            # Print the result
            print("\nAnswer:")
            print(result["result"])
            
            # Print source documents if available
            if result.get("source_documents"):
                print("\nSources:")
                for i, doc in enumerate(result["source_documents"]):
                    print(f"\n--- Source {i+1} ---")
                    print(f"File: {doc.metadata.get('source', doc.metadata.get('path', 'Unknown'))}")
                    print(f"Language: {doc.metadata.get('language', 'unknown')}")
                    print(f"Content: {doc.page_content[:150]}..." if len(doc.page_content) > 150 else f"Content: {doc.page_content}")
            
            # Tell the user how to continue the conversation
            print("\nYou can continue the conversation with another 'chat' command.")
            
        except Exception as chat_error:
            logger.error(f"Error during chat: {chat_error}")
            print("\nError occurred during chat processing. Falling back to showing relevant code snippets...\n")
            
            # Fallback to just showing code snippets
            code_snippets = agent.get_related_code(
                query_text=args.query,
                namespace=args.namespace,
                top_k=args.limit
            )
            
            if code_snippets:
                print(f"Found {len(code_snippets)} code snippets related to your query:")
                for i, snippet in enumerate(code_snippets):
                    print(f"\n--- Snippet {i+1} ---")
                    print(f"File: {snippet['file']}")
                    print(f"Language: {snippet['language']}")
                    print(f"Code:")
                    print(snippet['code'][:200] + "..." if len(snippet['code']) > 200 else snippet['code'])
            else:
                print("No relevant code snippets found.")
            
            print("\nNote: Your conversation history was not updated due to an error.")
            
        return 0
        
    except Exception as e:
        logger.error(f"Error chatting with codebase: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        print(f"Error chatting with codebase: {e}")
        return 1

def handle_related_command(args):
    """Handle the 'related' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Finding code related to query in index {args.index_name}: {args.query}")
    
    try:
        # Initialize Pinecone
        logger.info("Initializing Pinecone...")
        init_pinecone()
        
        # Create Code Agent instance
        agent = CodeAgent(index_name=args.index_name)
        
        # Get related code
        logger.info("Finding related code...")
        print(f"Query: {args.query}")
        
        # Execute the related code search
        results = agent.get_related_code(
            query_text=args.query,
            namespace=args.namespace,
            top_k=args.limit,
            use_mmr=args.use_mmr,
            mmr_diversity=args.diversity
        )
        
        # Print the results
        if results:
            print(f"\nFound {len(results)} code snippets related to your query:")
            for i, result in enumerate(results):
                print(f"\n--- Snippet {i+1} ---")
                print(f"File: {result['file']}")
                print(f"Language: {result['language']}")
                print(f"Code:")
                print(result['code'][:200] + "..." if len(result['code']) > 200 else result['code'])
        else:
            print("No related code snippets found.")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error finding related code: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        print(f"Error finding related code: {e}")
        return 1

def handle_configure_command(args):
    """Handle the 'configure' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    import os
    from dotenv import load_dotenv, set_key
    import getpass
    
    logger = logging.getLogger(__name__)
    logger.info("Configuring API keys and settings")
    
    # ANSI color codes
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    RESET = "\033[0m"
    
    # Load existing .env file if it exists
    env_file = ".env"
    existing_values = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
        "PINECONE_API_KEY": os.environ.get("PINECONE_API_KEY", ""),
        "LLM_MODEL": os.environ.get("LLM_MODEL", "claude-3-haiku-20240307")
    }
    
    if os.path.exists(env_file):
        # Make sure we're working with the latest values
        load_dotenv(env_file, override=True)
        # Update from environment after loading .env
        for key in existing_values:
            existing_values[key] = os.environ.get(key, existing_values[key])
        logger.info(f"Loaded existing configuration from {env_file}")
    
    # CLI values take precedence over existing values
    new_values = dict(existing_values)  # Start with existing values
    
    # Override with CLI arguments if provided
    if args.openai:
        new_values["OPENAI_API_KEY"] = args.openai
    if args.anthropic:
        new_values["ANTHROPIC_API_KEY"] = args.anthropic
    if args.pinecone:
        new_values["PINECONE_API_KEY"] = args.pinecone
    if args.model:
        new_values["LLM_MODEL"] = args.model
    
    # Interactive prompts if not non-interactive
    if not args.non_interactive:
        # Helper function for secure input
        def get_input(prompt, is_secret=False, default=None):
            display_prompt = f"{prompt} [{'*****' if default and is_secret else default or 'not set'}]: "
            if is_secret:
                value = getpass.getpass(display_prompt)
            else:
                try:
                    value = input(display_prompt)
                except EOFError:
                    print("\nInput operation failed.")
                    return default or ""
            return value if value else default or ""
        
        print(f"{BLUE}═════════════════════════════════════════{RESET}")
        print(f"{BLUE}    Codebase Indexer Configuration        {RESET}")
        print(f"{BLUE}═════════════════════════════════════════{RESET}")
        print(f"\nEnter your API keys below. Press Enter to keep existing values.")
        print(f"\n{YELLOW}Note: Keys are stored in {env_file} and not sent anywhere else.{RESET}")
        
        # Get API keys
        new_values["OPENAI_API_KEY"] = get_input(
            "OpenAI API Key (for embeddings)", 
            is_secret=True, 
            default=new_values["OPENAI_API_KEY"]
        )
        
        new_values["ANTHROPIC_API_KEY"] = get_input(
            "Anthropic API Key (for Claude)", 
            is_secret=True, 
            default=new_values["ANTHROPIC_API_KEY"]
        )
        
        new_values["PINECONE_API_KEY"] = get_input(
            "Pinecone API Key (for vector database)", 
            is_secret=True, 
            default=new_values["PINECONE_API_KEY"]
        )
        
        # Claude Model selection
        print(f"\n{BLUE}Available Claude Models:{RESET}")
        print("1. claude-3-haiku-20240307 (fast, cost-effective)")
        print("2. claude-3-sonnet-20240229 (balanced)")
        print("3. claude-3-opus-20240229 (highest quality)")
        print("4. Other (specify)")
        
        model_choice = get_input(f"Select model [1-4]", default="1")
        if model_choice == "1":
            new_values["LLM_MODEL"] = "claude-3-haiku-20240307"
        elif model_choice == "2":
            new_values["LLM_MODEL"] = "claude-3-sonnet-20240229"
        elif model_choice == "3":
            new_values["LLM_MODEL"] = "claude-3-opus-20240229"
        elif model_choice == "4":
            custom_model = get_input("Enter custom model name", default=new_values["LLM_MODEL"])
            new_values["LLM_MODEL"] = custom_model
    
    # Write the new values to .env file
    try:
        # Create the .env file if it doesn't exist
        if not os.path.exists(env_file):
            with open(env_file, "w") as f:
                pass
            logger.info(f"Created new .env file at {env_file}")
        
        # Write each key
        for key, value in new_values.items():
            if value:  # Only write non-empty values
                set_key(env_file, key, value)
        
        print(f"{GREEN}✓ Configuration saved to {env_file}{RESET}")
        
        # Check for missing keys without using validation logic
        missing_keys = [k for k, v in new_values.items() 
                        if k in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "PINECONE_API_KEY"] and not v]
        
        if missing_keys:
            print(f"{YELLOW}Note: Some API keys are not set: {', '.join(missing_keys)}{RESET}")
            print(f"{YELLOW}You can set them later by running 'codebase-indexer configure' again.{RESET}")
        else:
            print(f"{GREEN}✅ All API keys are set. You're ready to use Codebase Indexer!{RESET}")
            print(f"\nTry: codebase-indexer index --path /path/to/your/codebase")
        
        return 0
            
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        print(f"Error saving configuration: {e}")
        return 1

def handle_command(args):
    """Handle the command based on args.command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    # Map commands to handlers
    command_handlers = {
        "index": handle_index_command,
        "list": handle_list_command,
        "analyze": handle_analyze_command,
        "scan": handle_scan_command,
        "delete": handle_delete_command,
        "stats": handle_stats_command,
        "list-indexes": handle_list_indexes_command,
        "query": handle_query_command,
        "chat": handle_chat_command,
        "related": handle_related_command,
        "configure": handle_configure_command,
    }
    
    if args.command in command_handlers:
        return command_handlers[args.command](args)
    else:
        return 1