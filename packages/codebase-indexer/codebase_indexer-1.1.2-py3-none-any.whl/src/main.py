#!/usr/bin/env python3
"""
Codebase Indexer - A tool for indexing and querying large codebases
"""
import sys
import os
import logging
from dotenv import load_dotenv

# Load environment variables using dotenv before importing other modules
env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(env_file):
    # Let dotenv handle the .env file loading
    load_dotenv(env_file)

from src.utils.config import validate_api_keys
from src.utils.logger import setup_logger
from src.utils.commands import setup_arg_parser, handle_command

def main():
    """Main entry point for the codebase indexer CLI."""
    # Parse arguments
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(log_level)
    logger.info("Starting codebase indexer")
    
    # Commands that don't need API keys
    skip_validation_commands = ["list", "analyze", "scan", "configure"]
    
    # Only validate API keys for commands that need them
    if args.command and args.command not in skip_validation_commands:
        try:
            # Simple API key validation
            validate_api_keys()
        except ValueError as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")
            return 1
    
    if args.command:
        return handle_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())