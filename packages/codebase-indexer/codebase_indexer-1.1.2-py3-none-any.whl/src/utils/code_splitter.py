"""
Language-specific code splitter for better code chunking
This module implements specialized text splitters for different programming languages.
"""
import re
import logging
from typing import List, Dict, Optional, Callable, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Logger
logger = logging.getLogger(__name__)

# Default separators for different programming languages
DEFAULT_PYTHON_SEPARATORS = [
    # Class and function definitions
    "\nclass ", "\ndef ", "\n\tdef ", "\n    def ",
    # Module-level statements
    "\nimport ", "\nfrom ", 
    # Paragraph breaks
    "\n\n", 
    # Line breaks
    "\n", 
    # Word breaks
    " ", 
    # Character level
    ""
]

DEFAULT_JAVASCRIPT_SEPARATORS = [
    # Function and class definitions
    "\nfunction ", "\nclass ", "\nconst ", "\nlet ", "\nvar ",
    # Arrow functions
    "() => {", ") => {",
    # Module level
    "\nimport ", "\nexport ",
    # Paragraph breaks
    "\n\n", 
    # Line breaks
    "\n", 
    # Word breaks
    " ", 
    # Character level
    ""
]

DEFAULT_JAVA_SEPARATORS = [
    # Classes and methods
    "\npublic class ", "\nprivate class ", "\nprotected class ",
    "\npublic static ", "\nprivate static ", "\nprotected static ",
    "\npublic ", "\nprivate ", "\nprotected ",
    # Paragraph breaks
    "\n\n", 
    # Line breaks
    "\n", 
    # Word breaks
    " ", 
    # Character level
    ""
]

# Generic fallback separators
DEFAULT_CODE_SEPARATORS = [
    # Function-like patterns
    "\nfunction ", "\ndef ", "\nvoid ", "\nint ", "\nstring ", 
    "\nbool ", "\nfloat ", "\ndouble ", "\nvar ", "\nlet ", "\nconst ",
    # Class-like patterns
    "\nclass ", "\nstruct ", "\nenum ", "\ninterface ",
    # Import-like patterns
    "\nimport ", "\nfrom ", "\nusing ", "\nrequire ",
    # Paragraph breaks
    "\n\n", 
    # Line breaks
    "\n", 
    # Block separators
    "{", "}", 
    # Word breaks
    " ", 
    # Character level
    ""
]

# Mapping from language to separators
LANGUAGE_SEPARATORS = {
    "python": DEFAULT_PYTHON_SEPARATORS,
    "javascript": DEFAULT_JAVASCRIPT_SEPARATORS,
    "typescript": DEFAULT_JAVASCRIPT_SEPARATORS,
    "java": DEFAULT_JAVA_SEPARATORS,
    "cpp": DEFAULT_JAVA_SEPARATORS,
    "c": DEFAULT_JAVA_SEPARATORS,
    "csharp": DEFAULT_JAVA_SEPARATORS,
}

def get_language_specific_separators(language: str) -> List[str]:
    """Get language-specific separators for text splitting.
    
    Args:
        language: Programming language name.
    
    Returns:
        List of separator strings.
    """
    return LANGUAGE_SEPARATORS.get(language.lower(), DEFAULT_CODE_SEPARATORS)

def create_code_splitter(
    language: Optional[str] = None,
    chunk_size: int = 500, 
    chunk_overlap: int = 50,
    separators: Optional[List[str]] = None,
) -> RecursiveCharacterTextSplitter:
    """Create a language-specific code splitter.
    
    Args:
        language: Programming language for the code.
        chunk_size: Size of chunks to create.
        chunk_overlap: Overlap between chunks.
        separators: Custom separators to use (overrides language defaults).
        
    Returns:
        A RecursiveCharacterTextSplitter configured for the language.
    """
    if separators is None and language is not None:
        separators = get_language_specific_separators(language)
    elif separators is None:
        separators = DEFAULT_CODE_SEPARATORS
    
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        keep_separator=True
    )

def split_code_with_metadata(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[Document]:
    """Split code documents using language-specific splitters.
    
    This function tries to use language-specific splitters based on the
    language metadata in each document.
    
    Args:
        documents: List of Document objects containing code.
        chunk_size: Size of chunks to create.
        chunk_overlap: Overlap between chunks.
        
    Returns:
        List of chunked Document objects.
    """
    chunks: List[Document] = []
    
    # Group documents by language
    language_docs: Dict[str, List[Document]] = {}
    
    for doc in documents:
        language = doc.metadata.get('language', 'unknown')
        if language not in language_docs:
            language_docs[language] = []
        language_docs[language].append(doc)
    
    # Process each language group with appropriate splitter
    for language, docs in language_docs.items():
        splitter = create_code_splitter(
            language=language,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        logger.info(f"Splitting {len(docs)} {language} documents")
        language_chunks = splitter.split_documents(docs)
        chunks.extend(language_chunks)
        
        logger.info(f"Created {len(language_chunks)} chunks from {language} documents")
    
    return chunks

def enhance_code_chunks(chunks: List[Document]) -> List[Document]:
    """Enhance code chunks with additional metadata and preprocessing.
    
    This function adds useful metadata and makes code chunks more meaningful.
    
    Args:
        chunks: List of Document objects containing code chunks.
        
    Returns:
        Enhanced Document objects.
    """
    enhanced_chunks = []
    
    for chunk in chunks:
        # Copy existing metadata
        new_metadata = chunk.metadata.copy()
        
        # Extract function/class names from the chunk if possible
        language = new_metadata.get('language', 'unknown')
        content = chunk.page_content
        
        # Add code structure metadata
        code_elements = extract_code_elements(content, language)
        for key, value in code_elements.items():
            if value:  # Only add non-empty values
                new_metadata[key] = value
                
        # Create enhanced chunk
        enhanced_chunk = Document(
            page_content=content,
            metadata=new_metadata
        )
        enhanced_chunks.append(enhanced_chunk)
    
    return enhanced_chunks

def extract_code_elements(code: str, language: str) -> Dict[str, Any]:
    """Extract important code elements like function names, class names, etc.
    
    Args:
        code: The code content.
        language: The programming language.
        
    Returns:
        Dictionary with extracted elements.
    """
    elements = {
        "functions": [],
        "classes": [],
        "imports": [],
        "code_type": "unknown"
    }
    
    # Simple pattern matching based on language
    if language == "python":
        # Extract functions
        function_matches = re.findall(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)
        elements["functions"] = function_matches
        
        # Extract classes
        class_matches = re.findall(r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)", code)
        elements["classes"] = class_matches
        
        # Extract imports
        import_matches = re.findall(r"import\s+([a-zA-Z_][a-zA-Z0-9_\.]*)", code)
        from_import_matches = re.findall(r"from\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s+import", code)
        elements["imports"] = import_matches + from_import_matches
        
    elif language in ["javascript", "typescript"]:
        # Extract functions (including arrow functions and methods)
        function_matches = re.findall(r"function\s+([a-zA-Z_][a-zA-Z0-9_]*)", code)
        method_matches = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*{", code)
        elements["functions"] = function_matches + method_matches
        
        # Extract classes
        class_matches = re.findall(r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)", code)
        elements["classes"] = class_matches
        
        # Extract imports
        import_matches = re.findall(r"import\s+.*from\s+['\"]([^'\"]+)['\"]", code)
        elements["imports"] = import_matches
    
    # Determine code type
    if elements["classes"]:
        elements["code_type"] = "class_definition"
    elif elements["functions"]:
        elements["code_type"] = "function_definition"
    elif elements["imports"]:
        elements["code_type"] = "import_section"
    else:
        elements["code_type"] = "code_fragment"
    
    return elements