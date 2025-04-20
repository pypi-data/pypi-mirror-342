#!/usr/bin/env python3
"""
Codebase Indexer - A tool for indexing and querying large codebases
"""
import sys
import logging

from utils.config import validate_api_keys
from utils.logger import setup_logger
from utils.commands import setup_arg_parser, handle_command

def main():
    """Main entry point for the codebase indexer CLI."""
    # Parse arguments
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(log_level)
    logger.info("Starting codebase indexer")
    
    # Skip API key validation for commands that don't use external services
    skip_validation_commands = ["list", "analyze", "scan"]
    
    if args.command not in skip_validation_commands:
        try:
            # Validate API keys
            validate_api_keys()
        except ValueError as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")
            print("API keys are required for this command.")
            print("Use the 'configure' command to set up your API keys:")
            print("  codebase-indexer configure")
            return 1
    
    if args.command:
        return handle_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())