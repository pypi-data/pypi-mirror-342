#!/usr/bin/env python3
"""
Verify that all required dependencies are installed and API keys are set.
This script can be run to check that the environment is properly set up.
"""

import sys
import importlib
import os
from dotenv import load_dotenv

def check_package(package_name):
    """Check if a package is installed."""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def main():
    # List of required packages
    required_packages = [
        "langchain",
        "langchain_community",
        "langchain_openai",
        "langchain_anthropic",
        "langchain_pinecone",
        "openai",
        "pinecone",
        "anthropic",
        "dotenv",  # python-dotenv package is imported as dotenv
        "tiktoken",
    ]
    
    print("Checking required packages...")
    missing_packages = []
    
    for package in required_packages:
        if check_package(package):
            print(f"✅ {package}")
        else:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n⚠️ Missing packages. Please install them with:")
        print(f"pip install {' '.join(missing_packages)}")
        return 1
    
    # Check for API keys
    print("\nChecking API keys...")
    load_dotenv()
    
    required_env_vars = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "PINECONE_API_KEY",
    ]
    
    missing_env_vars = []
    
    for var in required_env_vars:
        value = os.getenv(var)
        if value:
            # Don't print the actual API key value for security
            print(f"✅ {var}")
        else:
            print(f"❌ {var}")
            missing_env_vars.append(var)
    
    if missing_env_vars:
        print("\n⚠️ Missing environment variables. Please add them to your .env file:")
        for var in missing_env_vars:
            print(f"{var}=your-{var.lower().replace('_', '-')}")
        return 1
    
    print("\n✅ All dependencies and API keys are properly configured!")
    return 0

if __name__ == "__main__":
    sys.exit(main())