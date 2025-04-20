import os
import logging
import fnmatch
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils.config import CHUNK_SIZE, CHUNK_OVERLAP

# Logger
logger = logging.getLogger(__name__)

# Common code file extensions to include
CODE_EXTENSIONS = [
    # Python
    "*.py", "*.pyi", "*.ipynb",
    # JavaScript/TypeScript
    "*.js", "*.jsx", "*.ts", "*.tsx", "*.vue", "*.svelte",
    # Java
    "*.java", "*.scala", "*.kt", "*.groovy",
    # C/C++
    "*.c", "*.cpp", "*.cc", "*.cxx", "*.h", "*.hpp", "*.hxx",
    # C#
    "*.cs", "*.vb",
    # Go
    "*.go",
    # Rust
    "*.rs",
    # Ruby
    "*.rb",
    # PHP
    "*.php",
    # Swift
    "*.swift",
    # Kotlin
    "*.kt",
    # Shell scripts
    "*.sh", "*.bash", "*.zsh",
    # Other languages
    "*.lua", "*.pl", "*.r", "*.dart", "*.elm", "*.ex", "*.exs",
    # Web
    "*.html", "*.htm", "*.css", "*.scss", "*.sass", "*.less",
    # Config
    "*.xml", "*.json", "*.yaml", "*.yml", "*.toml", "*.ini", "*.conf",
    # Documentation
    "*.md", "*.rst", "*.txt",
]

# Default directories to ignore
IGNORE_DIRS = [
    ".git",
    ".github",
    "node_modules",
    "venv",
    "env",
    ".env",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "site-packages",
    "vendor",
]

# Default files to ignore
IGNORE_FILES = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.so",
    "*.dll",
    "*.class",
    "*.exe",
    "*.bin",
    "*.dat",
    "*.pkl",
    "*.db",
    "*.sqlite",
    "*.log",
]

def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        True if the file is binary, False otherwise.
    """
    # Check file extension first
    _, ext = os.path.splitext(file_path)
    if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', 
                       '.pdf', '.zip', '.tar', '.gz', '.tgz', '.rar', 
                       '.7z', '.exe', '.dll', '.so', '.dylib', '.bin',
                       '.dat', '.o', '.obj', '.class']:
        return True
    
    # Try to open the file as text
    try:
        with open(file_path, 'tr') as f:
            chunk = f.read(1024)
            return '\0' in chunk  # If null byte is found, it's likely binary
    except UnicodeDecodeError:
        return True
    except Exception as e:
        logger.warning(f"Error checking if file is binary: {e}")
        return True

def should_include_file(file_path: str, 
                        extensions: Optional[List[str]] = None,
                        ignore_patterns: Optional[List[str]] = None) -> bool:
    """Check if a file should be included.
    
    Args:
        file_path: Path to the file.
        extensions: List of file extensions to include.
        ignore_patterns: List of file patterns to ignore.
        
    Returns:
        True if the file should be included, False otherwise.
    """
    # Skip hidden files and directories
    if os.path.basename(file_path).startswith('.'):
        return False
    
    # Skip binary files
    if is_binary_file(file_path):
        return False
    
    # Check ignore patterns
    if ignore_patterns:
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return False
    
    # Check file extension if provided
    if extensions:
        return any(fnmatch.fnmatch(file_path, pattern) for pattern in extensions)
    
    # Default: include all code file extensions
    return any(fnmatch.fnmatch(file_path, pattern) for pattern in CODE_EXTENSIONS)

def get_file_language(file_path: str) -> str:
    """Determine the programming language of a file based on its extension.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        The programming language name.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    # Map file extensions to languages
    language_map = {
        '.py': 'python',
        '.pyi': 'python',
        '.ipynb': 'jupyter',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.vue': 'vue',
        '.svelte': 'svelte',
        '.java': 'java',
        '.scala': 'scala',
        '.kt': 'kotlin',
        '.groovy': 'groovy',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.hxx': 'cpp',
        '.cs': 'csharp',
        '.vb': 'vb',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'bash',
        '.lua': 'lua',
        '.pl': 'perl',
        '.r': 'r',
        '.dart': 'dart',
        '.elm': 'elm',
        '.ex': 'elixir',
        '.exs': 'elixir',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.xml': 'xml',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.conf': 'config',
        '.md': 'markdown',
        '.rst': 'rst',
        '.txt': 'text',
    }
    
    return language_map.get(ext, 'unknown')

def scan_codebase(codebase_path: str, 
                 extensions: Optional[List[str]] = None,
                 ignore_dirs: Optional[List[str]] = None,
                 ignore_files: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Scan a codebase and collect metadata about the files.
    
    Args:
        codebase_path: Path to the codebase directory.
        extensions: List of file extensions to include.
        ignore_dirs: List of directories to ignore.
        ignore_files: List of files to ignore.
        
    Returns:
        List of dictionaries containing metadata about each file.
    """
    if not os.path.exists(codebase_path):
        raise ValueError(f"Path does not exist: {codebase_path}")
    
    if not os.path.isdir(codebase_path):
        raise ValueError(f"Path is not a directory: {codebase_path}")
    
    if ignore_dirs is None:
        ignore_dirs = IGNORE_DIRS
    
    if ignore_files is None:
        ignore_files = IGNORE_FILES
    
    # Convert extensions to patterns if provided
    extension_patterns = None
    if extensions:
        extension_patterns = [f"*.{ext.lstrip('.')}" for ext in extensions]
    
    files_metadata = []
    
    for root, dirs, files in os.walk(codebase_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, codebase_path)
            
            # Skip ignored files
            if any(fnmatch.fnmatch(file, pattern) for pattern in ignore_files):
                continue
            
            # Check if file should be included
            if should_include_file(file_path, extension_patterns):
                try:
                    file_size = os.path.getsize(file_path)
                    file_language = get_file_language(file_path)
                    
                    files_metadata.append({
                        'path': file_path,
                        'rel_path': rel_path,
                        'language': file_language,
                        'size': file_size,
                        'extension': os.path.splitext(file_path)[1],
                    })
                except Exception as e:
                    logger.warning(f"Error processing file {file_path}: {e}")
    
    return files_metadata

def load_documents(codebase_path: str, 
                  extensions: Optional[List[str]] = None,
                  ignore_dirs: Optional[List[str]] = None,
                  ignore_files: Optional[List[str]] = None,
                  show_progress: bool = True):
    """Load documents from a codebase path.
    
    Args:
        codebase_path: Path to the codebase directory.
        extensions: List of file extensions to include.
        ignore_dirs: List of directories to ignore.
        ignore_files: List of files to ignore.
        show_progress: Whether to show a progress bar.
        
    Returns:
        List of Document objects.
    """
    if not os.path.exists(codebase_path):
        raise ValueError(f"Path does not exist: {codebase_path}")
    
    if not os.path.isdir(codebase_path):
        raise ValueError(f"Path is not a directory: {codebase_path}")
    
    # Convert extensions to patterns if provided
    extension_patterns = None
    if extensions:
        extension_patterns = [f"*.{ext.lstrip('.')}" for ext in extensions]
    else:
        extension_patterns = CODE_EXTENSIONS
    
    # Create glob pattern
    glob_pattern = "{" + ",".join(extension_patterns) + "}"
    
    # Print the glob pattern for debugging
    logger.info(f"Using glob pattern: {glob_pattern}")
    
    # Try the manual approach first
    logger.info("Attempting to load files manually...")
    
    documents = []
    for root, _, files in os.walk(codebase_path):
        # Skip ignored directories and hidden directories
        if any(ignored in root for ignored in (ignore_dirs or IGNORE_DIRS)) or os.path.basename(root).startswith('.'):
            continue
            
        for file in files:
            # Skip hidden files and ignored files
            if file.startswith('.') or any(fnmatch.fnmatch(file, pattern) for pattern in (ignore_files or IGNORE_FILES)):
                continue
                
            # Check if file extension matches
            if not any(fnmatch.fnmatch(file, pattern) for pattern in extension_patterns):
                continue
                
            file_path = os.path.join(root, file)
            
            # Skip binary files
            if is_binary_file(file_path):
                continue
                
            try:
                logger.info(f"Loading file: {file_path}")
                loader = TextLoader(file_path)
                file_docs = loader.load()
                documents.extend(file_docs)
            except Exception as e:
                logger.warning(f"Error loading file {file_path}: {e}")
    
    if not documents:
        # Fall back to DirectoryLoader as a last resort
        logger.warning("Manual loading found no documents, trying DirectoryLoader...")
        try:
            loader = DirectoryLoader(
                codebase_path,
                glob="**/*.py",  # Start with just Python files
                loader_cls=TextLoader,
                show_progress=show_progress
            )
            documents = loader.load()
        except Exception as e:
            logger.error(f"Error with DirectoryLoader: {e}")
            # Return empty list if all methods fail
            documents = []
    
    logger.info(f"Loaded {len(documents)} documents")
    
    # Add language metadata to documents
    for doc in documents:
        doc.metadata['language'] = get_file_language(doc.metadata['source'])
        doc.metadata['rel_path'] = os.path.relpath(doc.metadata['source'], codebase_path)
    
    return documents

def chunk_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Split documents into chunks using language-specific splitters.
    
    Args:
        documents: List of Document objects.
        chunk_size: Size of each chunk.
        chunk_overlap: Overlap between chunks.
        
    Returns:
        List of chunked Document objects.
    """
    from src.utils.code_splitter import split_code_with_metadata, enhance_code_chunks
    
    logger.info(f"Chunking documents with size={chunk_size}, overlap={chunk_overlap} using language-specific splitters...")
    
    try:
        # Use language-specific code splitting
        chunked_documents = split_code_with_metadata(
            documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        # Enhance chunks with additional metadata
        enhanced_chunks = enhance_code_chunks(chunked_documents)
        
        logger.info(f"Created and enhanced {len(enhanced_chunks)} chunks")
        return enhanced_chunks
        
    except Exception as e:
        logger.warning(f"Error using advanced code splitting: {e}. Falling back to basic splitter...")
        # Fallback to basic splitting if advanced splitting fails
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunked_documents = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunked_documents)} chunks with basic splitter")
        
        return chunked_documents