from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements file
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().strip().split("\n")

setup(
    name="codebase-indexer",
    version="1.2.0",  # Limited file types to Python, JS/TS, HTML, CSS, SCSS, MD, and Dockerfiles
    description="A command-line tool for indexing and querying large codebases using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rajwardhan Shinde",
    author_email="rajshinde55553@example.com",
    url="https://github.com/RajwardhanShinde/Code-Indexer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "codebase-indexer=bin.codebase_indexer:main",
            "indexer=bin.codebase_indexer:main",  # Shorter alias
            "code-indexer=bin.codebase_indexer:main",  # Another alias that might avoid issues
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="code, indexing, search, AI, embeddings, RAG, retrieval, Claude, OpenAI, Pinecone",
    python_requires=">=3.8",
    scripts=['bin/codebase-indexer.py'],  # Fallback script
)