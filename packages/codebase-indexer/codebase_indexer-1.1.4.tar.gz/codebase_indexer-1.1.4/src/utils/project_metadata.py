"""
Utilities for extracting project metadata from common project files
"""
import os
import json
import logging
import re
from typing import Dict, List, Any, Optional

# Logger
logger = logging.getLogger(__name__)

def parse_package_json(file_path: str) -> Dict[str, Any]:
    """Parse package.json file to extract project metadata.
    
    Args:
        file_path: Path to the package.json file.
        
    Returns:
        Dictionary containing project metadata.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        result = {
            'name': data.get('name'),
            'version': data.get('version'),
            'description': data.get('description'),
            'type': 'npm',
            'dependencies': data.get('dependencies', {}),
            'devDependencies': data.get('devDependencies', {}),
            'peerDependencies': data.get('peerDependencies', {}),
            'scripts': data.get('scripts', {}),
            'author': data.get('author'),
            'license': data.get('license'),
            'repository': data.get('repository'),
            'main': data.get('main'),
            'engines': data.get('engines', {})
        }
        
        return result
    except Exception as e:
        logger.error(f"Error parsing package.json at {file_path}: {e}")
        return {'error': str(e)}

def parse_setup_py(file_path: str) -> Dict[str, Any]:
    """Parse setup.py file to extract project metadata.
    
    Args:
        file_path: Path to the setup.py file.
        
    Returns:
        Dictionary containing project metadata.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'type': 'python',
        }
        
        # Extract project name
        name_match = re.search(r"name\s*=\s*['\"]([^'\"]+)['\"]", content)
        if name_match:
            result['name'] = name_match.group(1)
        
        # Extract version
        version_match = re.search(r"version\s*=\s*['\"]([^'\"]+)['\"]", content)
        if version_match:
            result['version'] = version_match.group(1)
        
        # Extract description
        description_match = re.search(r"description\s*=\s*['\"]([^'\"]+)['\"]", content)
        if description_match:
            result['description'] = description_match.group(1)
        
        # Extract install_requires
        install_requires_match = re.search(r"install_requires\s*=\s*\[(.*?)\]", content, re.DOTALL)
        if install_requires_match:
            requires_str = install_requires_match.group(1)
            requires = []
            for match in re.finditer(r"['\"]([^'\"]+)['\"]", requires_str):
                requires.append(match.group(1))
            result['dependencies'] = requires
        
        # Extract author
        author_match = re.search(r"author\s*=\s*['\"]([^'\"]+)['\"]", content)
        if author_match:
            result['author'] = author_match.group(1)
        
        # Extract license
        license_match = re.search(r"license\s*=\s*['\"]([^'\"]+)['\"]", content)
        if license_match:
            result['license'] = license_match.group(1)
        
        return result
    except Exception as e:
        logger.error(f"Error parsing setup.py at {file_path}: {e}")
        return {'error': str(e)}

def parse_requirements_txt(file_path: str) -> Dict[str, Any]:
    """Parse requirements.txt file to extract dependencies.
    
    Args:
        file_path: Path to the requirements.txt file.
        
    Returns:
        Dictionary containing dependencies.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Remove any comments at the end of the line
            line = line.split('#')[0].strip()
            
            dependencies.append(line)
        
        return {
            'type': 'python',
            'dependencies': dependencies
        }
    except Exception as e:
        logger.error(f"Error parsing requirements.txt at {file_path}: {e}")
        return {'error': str(e)}

def parse_cargo_toml(file_path: str) -> Dict[str, Any]:
    """Parse Cargo.toml file to extract project metadata for Rust projects.
    
    Args:
        file_path: Path to the Cargo.toml file.
        
    Returns:
        Dictionary containing project metadata.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'type': 'rust',
        }
        
        # Extract package section
        package_match = re.search(r'\[package\](.*?)(?=\[\w+\]|\Z)', content, re.DOTALL)
        if package_match:
            package_content = package_match.group(1)
            
            # Extract name
            name_match = re.search(r'name\s*=\s*"([^"]+)"', package_content)
            if name_match:
                result['name'] = name_match.group(1)
            
            # Extract version
            version_match = re.search(r'version\s*=\s*"([^"]+)"', package_content)
            if version_match:
                result['version'] = version_match.group(1)
            
            # Extract description
            description_match = re.search(r'description\s*=\s*"([^"]+)"', package_content)
            if description_match:
                result['description'] = description_match.group(1)
            
            # Extract authors
            authors_match = re.search(r'authors\s*=\s*\[(.*?)\]', package_content, re.DOTALL)
            if authors_match:
                authors_str = authors_match.group(1)
                authors = []
                for match in re.finditer(r'"([^"]+)"', authors_str):
                    authors.append(match.group(1))
                result['authors'] = authors
            
            # Extract license
            license_match = re.search(r'license\s*=\s*"([^"]+)"', package_content)
            if license_match:
                result['license'] = license_match.group(1)
        
        # Extract dependencies
        dependencies_match = re.search(r'\[dependencies\](.*?)(?=\[\w+\]|\Z)', content, re.DOTALL)
        if dependencies_match:
            dependencies_content = dependencies_match.group(1)
            dependencies = {}
            
            # Simple dependencies format: name = "version"
            for match in re.finditer(r'([a-zA-Z0-9_-]+)\s*=\s*"([^"]+)"', dependencies_content):
                dependencies[match.group(1)] = match.group(2)
            
            result['dependencies'] = dependencies
        
        return result
    except Exception as e:
        logger.error(f"Error parsing Cargo.toml at {file_path}: {e}")
        return {'error': str(e)}

def parse_gradle_build(file_path: str) -> Dict[str, Any]:
    """Parse build.gradle file to extract project metadata for Java/Kotlin projects.
    
    Args:
        file_path: Path to the build.gradle file.
        
    Returns:
        Dictionary containing project metadata.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'type': 'gradle',
        }
        
        # Extract group
        group_match = re.search(r"group\s*=\s*['\"]([^'\"]+)['\"]", content)
        if group_match:
            result['group'] = group_match.group(1)
        
        # Extract version
        version_match = re.search(r"version\s*=\s*['\"]([^'\"]+)['\"]", content)
        if version_match:
            result['version'] = version_match.group(1)
        
        # Extract dependencies
        dependencies_match = re.search(r'dependencies\s*{(.*?)}', content, re.DOTALL)
        if dependencies_match:
            dependencies_content = dependencies_match.group(1)
            dependencies = []
            
            for match in re.finditer(r"(implementation|testImplementation|api|compileOnly)\s*['\"]([^'\"]+)['\"]", dependencies_content):
                scope = match.group(1)
                dep = match.group(2)
                dependencies.append({
                    'scope': scope,
                    'dependency': dep
                })
            
            result['dependencies'] = dependencies
        
        return result
    except Exception as e:
        logger.error(f"Error parsing build.gradle at {file_path}: {e}")
        return {'error': str(e)}

def extract_project_metadata(project_path: str) -> Dict[str, Any]:
    """Extract metadata for a project.
    
    Args:
        project_path: Path to the project root directory.
        
    Returns:
        Dictionary containing project metadata.
    """
    result = {
        'path': project_path,
        'project_files': {},
        'language': 'unknown',
        'type': 'unknown',
    }
    
    try:
        # Check for common project files
        common_files = {
            'package.json': parse_package_json,
            'setup.py': parse_setup_py,
            'requirements.txt': parse_requirements_txt,
            'Cargo.toml': parse_cargo_toml,
            'build.gradle': parse_gradle_build,
            'build.gradle.kts': parse_gradle_build,
        }
        
        for filename, parser in common_files.items():
            file_path = os.path.join(project_path, filename)
            if os.path.isfile(file_path):
                result['project_files'][filename] = parser(file_path)
        
        # Determine project language and type
        if 'package.json' in result['project_files']:
            result['language'] = 'javascript/typescript'
            result['type'] = 'npm'
            result['name'] = result['project_files']['package.json'].get('name')
            result['version'] = result['project_files']['package.json'].get('version')
        elif 'setup.py' in result['project_files']:
            result['language'] = 'python'
            result['type'] = 'python'
            result['name'] = result['project_files']['setup.py'].get('name')
            result['version'] = result['project_files']['setup.py'].get('version')
        elif 'requirements.txt' in result['project_files']:
            result['language'] = 'python'
            result['type'] = 'python'
        elif 'Cargo.toml' in result['project_files']:
            result['language'] = 'rust'
            result['type'] = 'rust'
            result['name'] = result['project_files']['Cargo.toml'].get('name')
            result['version'] = result['project_files']['Cargo.toml'].get('version')
        elif 'build.gradle' in result['project_files'] or 'build.gradle.kts' in result['project_files']:
            result['language'] = 'java/kotlin'
            result['type'] = 'gradle'
            gradle_file = 'build.gradle' if 'build.gradle' in result['project_files'] else 'build.gradle.kts'
            result['group'] = result['project_files'][gradle_file].get('group')
            result['version'] = result['project_files'][gradle_file].get('version')
        
        # Try to infer the project type from directory structure if not determined
        if result['type'] == 'unknown':
            if os.path.isdir(os.path.join(project_path, 'src', 'main', 'java')):
                result['language'] = 'java'
                result['type'] = 'java'
            elif os.path.isdir(os.path.join(project_path, 'src', 'main', 'kotlin')):
                result['language'] = 'kotlin'
                result['type'] = 'kotlin'
            elif os.path.isdir(os.path.join(project_path, 'go')):
                result['language'] = 'go'
                result['type'] = 'go'
        
        return result
    
    except Exception as e:
        logger.error(f"Error extracting project metadata from {project_path}: {e}")
        result['error'] = str(e)
        return result