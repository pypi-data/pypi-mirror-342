#!/usr/bin/env python3
"""
Standalone script for running the codebase indexer.
This script will be installed in the user's PATH.
"""
import sys
import os
from dotenv import load_dotenv

def main():
    """Main entry point for the codebase indexer CLI."""
    # Add the parent directory of 'src' to the Python path if needed
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    # Look for a .env file in the current working directory first
    cwd_env_file = os.path.join(os.getcwd(), '.env')
    if os.path.exists(cwd_env_file):
        # Use python-dotenv to load environment variables
        load_dotenv(cwd_env_file)
    
    # Fallback to .env in the installation directory
    install_env_file = os.path.join(script_dir, '.env')
    if os.path.exists(install_env_file):
        # Use python-dotenv to load environment variables
        load_dotenv(install_env_file)
    
    # Now import can work
    try:
        from src.main import main as src_main
        return src_main()
    except ModuleNotFoundError:
        # If that doesn't work, try importing directly (for installed packages)
        try:
            # When installed as a package, import should work directly
            from codebase_indexer.main import main as src_main
            return src_main()
        except ModuleNotFoundError:
            print("ERROR: Could not import the main module.")
            print("This may be due to an installation issue.")
            print("Try reinstalling the package with: pip install --user codebase-indexer")
            return 1

if __name__ == "__main__":
    sys.exit(main())