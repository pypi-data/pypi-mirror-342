"""
Utilities for code analysis and language-specific parsing
"""
import os
import logging
import re
from typing import Dict, List, Any, Optional, Tuple

# Logger
logger = logging.getLogger(__name__)

def extract_functions_from_python(content: str) -> List[Dict[str, Any]]:
    """Extract function definitions from Python code.
    
    Args:
        content: The Python code content.
        
    Returns:
        List of dictionaries containing function metadata.
    """
    # Regular expression to match Python function definitions
    # This is a simplified version and might miss some edge cases
    pattern = r"(async\s+)?def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)(?:\s*->\s*([a-zA-Z0-9_\[\], \.]+))?\s*:"
    
    functions = []
    for match in re.finditer(pattern, content, re.DOTALL):
        is_async = bool(match.group(1))
        name = match.group(2)
        params = match.group(3)
        return_type = match.group(4)
        
        # Find the function body (simplified)
        start_pos = match.end()
        # This is a simplification; proper parsing would require understanding indentation
        
        functions.append({
            'name': name,
            'params': params,
            'return_type': return_type,
            'is_async': is_async,
            'start_pos': match.start(),
            'end_pos': start_pos,
            'type': 'function'
        })
    
    return functions

def extract_classes_from_python(content: str) -> List[Dict[str, Any]]:
    """Extract class definitions from Python code.
    
    Args:
        content: The Python code content.
        
    Returns:
        List of dictionaries containing class metadata.
    """
    # Regular expression to match Python class definitions
    pattern = r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:\((.*?)\))?\s*:"
    
    classes = []
    for match in re.finditer(pattern, content, re.DOTALL):
        name = match.group(1)
        inheritance = match.group(2)
        
        # Find the class body (simplified)
        start_pos = match.end()
        # This is a simplification; proper parsing would require understanding indentation
        
        classes.append({
            'name': name,
            'inheritance': inheritance,
            'start_pos': match.start(),
            'end_pos': start_pos,
            'type': 'class'
        })
    
    return classes

def extract_imports_from_python(content: str) -> List[Dict[str, Any]]:
    """Extract import statements from Python code.
    
    Args:
        content: The Python code content.
        
    Returns:
        List of dictionaries containing import metadata.
    """
    # Regular expressions to match import statements
    import_pattern = r"import\s+([\w\.]+)(?:\s+as\s+([\w]+))?"
    from_import_pattern = r"from\s+([\w\.]+)\s+import\s+(.+)"
    
    imports = []
    
    # Match 'import x' statements
    for match in re.finditer(import_pattern, content):
        module = match.group(1)
        alias = match.group(2)
        
        imports.append({
            'module': module,
            'alias': alias,
            'type': 'import'
        })
    
    # Match 'from x import y' statements
    for match in re.finditer(from_import_pattern, content):
        module = match.group(1)
        imported = match.group(2)
        
        # Split multiple imports (e.g., 'from x import y, z')
        for item in re.split(r',\s*', imported):
            parts = re.match(r'([\w\.]+)(?:\s+as\s+([\w]+))?', item.strip())
            if parts:
                name = parts.group(1)
                alias = parts.group(2)
                
                imports.append({
                    'module': module,
                    'name': name,
                    'alias': alias,
                    'type': 'from_import'
                })
    
    return imports

def extract_functions_from_javascript(content: str) -> List[Dict[str, Any]]:
    """Extract function definitions from JavaScript/TypeScript code.
    
    Args:
        content: The JavaScript/TypeScript code content.
        
    Returns:
        List of dictionaries containing function metadata.
    """
    # Regular expressions to match JS/TS function definitions
    # This is simplified and won't catch all cases
    patterns = [
        # function declaration: function name(params) {}
        r"function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\((.*?)\)\s*(?::\s*([a-zA-Z0-9_$\[\], \.]+))?\s*\{",
        # arrow function: const name = (params) => {}
        r"(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:async\s+)?\((.*?)\)\s*(?::\s*([a-zA-Z0-9_$\[\], \.]+))?\s*=>\s*\{",
        # method definition: name(params) {}
        r"([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\((.*?)\)\s*(?::\s*([a-zA-Z0-9_$\[\], \.]+))?\s*\{"
    ]
    
    functions = []
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.DOTALL):
            name = match.group(1)
            params = match.group(2)
            return_type = match.group(3) if len(match.groups()) >= 3 else None
            
            functions.append({
                'name': name,
                'params': params,
                'return_type': return_type,
                'start_pos': match.start(),
                'end_pos': match.end(),
                'type': 'function'
            })
    
    return functions

def extract_classes_from_javascript(content: str) -> List[Dict[str, Any]]:
    """Extract class definitions from JavaScript/TypeScript code.
    
    Args:
        content: The JavaScript/TypeScript code content.
        
    Returns:
        List of dictionaries containing class metadata.
    """
    # Regular expression to match JS/TS class definitions
    pattern = r"class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:extends\s+([a-zA-Z_$][a-zA-Z0-9_$]*))?(?:implements\s+([a-zA-Z_$][a-zA-Z0-9_$, ]*))?(?:\s*\{)"
    
    classes = []
    for match in re.finditer(pattern, content, re.DOTALL):
        name = match.group(1)
        extends = match.group(2)
        implements = match.group(3)
        
        classes.append({
            'name': name,
            'extends': extends,
            'implements': implements,
            'start_pos': match.start(),
            'end_pos': match.end(),
            'type': 'class'
        })
    
    return classes

def extract_imports_from_javascript(content: str) -> List[Dict[str, Any]]:
    """Extract import statements from JavaScript/TypeScript code.
    
    Args:
        content: The JavaScript/TypeScript code content.
        
    Returns:
        List of dictionaries containing import metadata.
    """
    # Regular expressions to match import statements
    import_default_pattern = r"import\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s+from\s+['\"](.+)['\"]"
    import_named_pattern = r"import\s+\{\s*(.+?)\s*\}\s+from\s+['\"](.+)['\"]"
    import_all_pattern = r"import\s+\*\s+as\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s+from\s+['\"](.+)['\"]"
    
    imports = []
    
    # Match default imports: import Name from 'module'
    for match in re.finditer(import_default_pattern, content):
        name = match.group(1)
        module = match.group(2)
        
        imports.append({
            'name': name,
            'module': module,
            'type': 'default_import'
        })
    
    # Match named imports: import { Name1, Name2 as Alias } from 'module'
    for match in re.finditer(import_named_pattern, content):
        names_str = match.group(1)
        module = match.group(2)
        
        # Parse the named imports
        for item in re.split(r',\s*', names_str):
            parts = re.match(r'([\w$]+)(?:\s+as\s+([\w$]+))?', item.strip())
            if parts:
                name = parts.group(1)
                alias = parts.group(2)
                
                imports.append({
                    'name': name,
                    'alias': alias,
                    'module': module,
                    'type': 'named_import'
                })
    
    # Match namespace imports: import * as Name from 'module'
    for match in re.finditer(import_all_pattern, content):
        alias = match.group(1)
        module = match.group(2)
        
        imports.append({
            'alias': alias,
            'module': module,
            'type': 'namespace_import'
        })
    
    return imports

def analyze_code(file_path: str) -> Dict[str, Any]:
    """Analyze a code file and extract metadata.
    
    Args:
        file_path: Path to the code file.
        
    Returns:
        Dictionary containing code metadata.
    """
    try:
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'path': file_path,
            'language': get_language_from_extension(ext),
            'functions': [],
            'classes': [],
            'imports': [],
            'size': len(content),
            'lines': content.count('\n') + 1
        }
        
        # Apply language-specific analysis
        if ext in ['.py', '.pyi']:
            result['functions'] = extract_functions_from_python(content)
            result['classes'] = extract_classes_from_python(content)
            result['imports'] = extract_imports_from_python(content)
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            result['functions'] = extract_functions_from_javascript(content)
            result['classes'] = extract_classes_from_javascript(content)
            result['imports'] = extract_imports_from_javascript(content)
        
        return result
    
    except Exception as e:
        logger.warning(f"Error analyzing file {file_path}: {e}")
        return {
            'path': file_path,
            'error': str(e)
        }

def get_language_from_extension(ext: str) -> str:
    """Get language name from file extension.
    
    Args:
        ext: File extension.
        
    Returns:
        Language name.
    """
    language_map = {
        # Python
        '.py': 'python',
        '.pyi': 'python',
        '.ipynb': 'jupyter',
        # JavaScript/TypeScript
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.vue': 'vue',
        '.svelte': 'svelte',
        # Java
        '.java': 'java',
        '.scala': 'scala',
        '.kt': 'kotlin',
        '.groovy': 'groovy',
        # C/C++
        '.c': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.hxx': 'cpp',
        # C#
        '.cs': 'csharp',
        '.vb': 'vb',
        # Go
        '.go': 'go',
        # Rust
        '.rs': 'rust',
        # Ruby
        '.rb': 'ruby',
        # PHP
        '.php': 'php',
        # Swift
        '.swift': 'swift',
        # Shell
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'bash',
        # Web
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        # Config
        '.xml': 'xml',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.conf': 'config',
        # Documentation
        '.md': 'markdown',
        '.rst': 'rst',
        '.txt': 'text',
    }
    
    return language_map.get(ext, 'unknown')