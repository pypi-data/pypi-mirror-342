#!/usr/bin/env python3
"""
Standalone script for running the codebase indexer.
This script will be installed in the user's PATH.
"""
import sys
import os

# Add the parent directory of 'src' to the Python path if needed
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Now import can work
try:
    from src.main import main
except ModuleNotFoundError:
    # If that doesn't work, try importing directly (for installed packages)
    try:
        # When installed as a package, import should work directly
        from codebase_indexer.main import main
    except ModuleNotFoundError:
        print("ERROR: Could not import the main module.")
        print("This may be due to an installation issue.")
        print("Try reinstalling the package with: pip install --user codebase-indexer")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())