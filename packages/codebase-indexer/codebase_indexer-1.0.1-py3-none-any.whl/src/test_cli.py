#!/usr/bin/env python3
"""
Test script for the command-line interface.
This script doesn't require API keys and will
only test the parts of the CLI that don't need external services.
"""
import os
import sys
import logging
import argparse
from src.utils.logger import setup_logger
from src.utils.file_utils import scan_codebase
from src.utils.project_metadata import extract_project_metadata
from src.utils.code_analysis import analyze_code

def setup_test_arg_parser():
    """Set up the command-line argument parser for testing.
    
    Returns:
        ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Test script for the codebase indexer CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List files in a codebase")
    list_parser.add_argument("--path", required=True, help="Path to the codebase directory")
    list_parser.add_argument("--extensions", help="Comma-separated list of file extensions to include (e.g., py,js,java)")
    list_parser.add_argument("--count", action="store_true", help="Show file count by extension")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a codebase")
    analyze_parser.add_argument("--path", required=True, help="Path to the codebase directory")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan a codebase and output metadata")
    scan_parser.add_argument("--path", required=True, help="Path to the codebase directory")
    scan_parser.add_argument("--extensions", help="Comma-separated list of file extensions to include (e.g., py,js,java)")
    
    # File command
    file_parser = subparsers.add_parser("file", help="Analyze a single file")
    file_parser.add_argument("--path", required=True, help="Path to the file")
    
    # Common options
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    return parser

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
        
        return 0
    
    except Exception as e:
        logger.error(f"Error scanning codebase: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        return 1

def handle_file_command(args):
    """Handle the 'file' command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Analyzing file: {args.path}")
    
    # Validate path
    if not os.path.exists(args.path):
        logger.error(f"File does not exist: {args.path}")
        return 1
    
    if not os.path.isfile(args.path):
        logger.error(f"Path is not a file: {args.path}")
        return 1
    
    try:
        # Analyze file
        analysis = analyze_code(args.path)
        
        # Print analysis
        print(f"File: {args.path}")
        print(f"Language: {analysis['language']}")
        print(f"Size: {analysis['size']} bytes")
        print(f"Lines: {analysis['lines']}")
        
        if 'functions' in analysis and analysis['functions']:
            print("\nFunctions:")
            for func in analysis['functions']:
                print(f"- {func['name']}")
        
        if 'classes' in analysis and analysis['classes']:
            print("\nClasses:")
            for cls in analysis['classes']:
                print(f"- {cls['name']}")
        
        if 'imports' in analysis and analysis['imports']:
            print("\nImports:")
            for imp in analysis['imports']:
                if imp['type'] == 'import':
                    print(f"- import {imp['module']}")
                elif imp['type'] == 'from_import':
                    print(f"- from {imp['module']} import {imp['name']}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error analyzing file: {e}")
        if args.verbose:
            logger.exception("Exception details:")
        return 1

def handle_test_command(args):
    """Handle the command based on args.command.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: Return code (0 for success).
    """
    # Map commands to handlers
    command_handlers = {
        "list": handle_list_command,
        "analyze": handle_analyze_command,
        "scan": handle_scan_command,
        "file": handle_file_command,
    }
    
    if args.command in command_handlers:
        return command_handlers[args.command](args)
    else:
        return 1

def main():
    """Main entry point for the test CLI."""
    # Parse arguments
    parser = setup_test_arg_parser()
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(log_level)
    
    if args.command:
        return handle_test_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())