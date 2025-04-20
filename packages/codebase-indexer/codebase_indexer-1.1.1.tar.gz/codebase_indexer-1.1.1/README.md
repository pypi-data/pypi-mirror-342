# Large Codebase Indexer

A command-line tool for indexing large codebases and enabling AI-powered queries.

## Overview

This tool allows you to index any codebase and query it using natural language. It leverages:

- OpenAI's embedding model for code semantics
- Pinecone vector database for efficient storage and retrieval
- Claude LLM for high-quality responses
- LangChain framework for integrating all components

## Installation

### Option 1: Install from PyPI (recommended)

```bash
# Install the package
pip install codebase-indexer

# Configure your API keys interactively
codebase-indexer configure
```

If you encounter "command not found" errors, use our installer scripts:

**For macOS/Linux:**
```bash
curl -O https://raw.githubusercontent.com/yourusername/indexer/main/easy-install.sh
chmod +x easy-install.sh
./easy-install.sh
```

**For Windows:**
```cmd
curl -O https://raw.githubusercontent.com/yourusername/indexer/main/install-windows.bat
install-windows.bat
```

### Option 2: Install from source

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/indexer.git
   cd indexer
   ```

2. Install the package in development mode:
   ```bash
   # Create a virtual environment (recommended)
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install in development mode
   pip install -e .
   ```

3. Create a `.env` file with your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

### Option 3: Quick setup (using the install script)

```bash
./install.sh
```

### API Keys

This tool requires API keys for:
- OpenAI (for embeddings)
- Anthropic (for Claude LLM)
- Pinecone (for vector storage)

You can get these keys by signing up at:
- [OpenAI](https://platform.openai.com/)
- [Anthropic](https://www.anthropic.com/)
- [Pinecone](https://www.pinecone.io/)

#### Setting up API keys

You can configure API keys using the interactive CLI:

```bash
# Interactive configuration
codebase-indexer configure

# Non-interactive configuration
codebase-indexer configure --openai=your-openai-key --anthropic=your-anthropic-key --pinecone=your-pinecone-key
```

The configuration command will:
1. Create a `.env` file if it doesn't exist
2. Prompt for missing API keys (or use the ones provided via command-line arguments)
3. Allow you to select the Claude model to use
4. Validate that all required keys are set

## Usage

### Indexing a Codebase

Index a codebase to create vector embeddings stored in Pinecone:

```bash
python src/main.py index --path /path/to/your/codebase --index-name your-index-name
```

Options:
- `--path`: Path to the codebase directory (required)
- `--index-name`: Name of the Pinecone index (default: "codebase-index")
- `--namespace`: Namespace within the index for this codebase (default: directory name)
- `--chunk-size`: Size of code chunks (default: 800, recommended range: 500-1500)
- `--chunk-overlap`: Overlap between chunks (default: 150, recommended range: 50-200)
- `--extensions`: Comma-separated list of file extensions to index (e.g., py,js,java)
- `--batch-size`: Batch size for indexing (default: 100)

The tool now uses language-specific code chunking that intelligently splits code based on its structure (functions, classes, etc.) rather than just character count. This results in more meaningful chunks that preserve code context.

### Listing Files in a Codebase

List all files in a codebase or show file count by extension:

```bash
python src/main.py list --path /path/to/your/codebase --extensions py,js,java
python src/main.py list --path /path/to/your/codebase --count
```

### Analyzing a Codebase

Analyze a codebase to extract project metadata:

```bash
python src/main.py analyze --path /path/to/your/codebase
```

### Scanning a Codebase

Scan a codebase to get information about files and languages:

```bash
python src/main.py scan --path /path/to/your/codebase
```

### Managing Indexes

List all Pinecone indexes:

```bash
python src/main.py list-indexes
```

Get statistics about an index:

```bash
python src/main.py stats --index-name your-index-name
```

Delete an index or namespace:

```bash
python src/main.py delete --index-name your-index-name
python src/main.py delete --index-name your-index-name --namespace your-namespace
```

### Querying the Indexed Codebase

Query the indexed codebase using natural language:

```bash
python src/main.py query --query "What does the authenticate_user function do?" --index-name your-index-name --namespace your-namespace
```

Options:
- `--query`: The query string (required)
- `--index-name`: Name of the Pinecone index (default: "codebase-index")
- `--namespace`: Namespace to query in Pinecone
- `--limit`: Maximum number of results to return (default: 5)
- `--no-mmr`: Disable Maximum Marginal Relevance retrieval (MMR is enabled by default)
- `--diversity`: Diversity parameter for MMR (0-1, default: 0.3)

The tool now uses Maximum Marginal Relevance (MMR) by default, which balances relevance with diversity in search results. This helps avoid redundant code snippets and provides more comprehensive answers.

### Chat with Conversation History

Have a conversation with the codebase, maintaining context between questions:

```bash
python src/main.py chat --query "How does the file loading work?" --index-name your-index-name
python src/main.py chat --query "What parameters does it accept?" --index-name your-index-name
```

### Find Related Code

Get code snippets related to a query without generating an answer:

```bash
python src/main.py related --query "error handling" --index-name your-index-name --limit 10
```

### Testing the CLI (without API keys)

You can use the test CLI script for commands that don't require API keys:

```bash
python src/test_cli.py list --path /path/to/your/codebase --count
python src/test_cli.py analyze --path /path/to/your/codebase
python src/test_cli.py file --path /path/to/your/codebase/some_file.py
```

## Command-Line Interface

The tool provides the following commands:

- `index`: Index a codebase
- `list`: List files in a codebase
- `analyze`: Analyze a codebase and extract project metadata
- `scan`: Scan a codebase and output file statistics
- `list-indexes`: List all Pinecone indexes
- `stats`: Show statistics about an index
- `delete`: Delete an index or namespace
- `query`: Query the indexed codebase
- `chat`: Chat with the codebase using conversation history
- `related`: Get code snippets related to a query

Use `--help` with any command to see available options:

```bash
python src/main.py --help
python src/main.py index --help
```

## Development Status

This project is being developed in phases:

1. ✅ Environment Setup
2. ✅ Command-Line Tool Framework 
3. ✅ Codebase Indexing
4. ✅ RAG System and Agent Development
5. 🔜 Testing, Refinement, and Deployment

## Project Structure

```
indexer/
├── docs/
│   └── ADR.md           # Architecture Decision Record
├── src/
│   ├── agents/          # RAG agent implementation
│   ├── indexers/        # Code indexing functionality
│   ├── models/          # OpenAI and Claude model wrappers
│   ├── utils/           # Utility functions
│   ├── main.py          # Main CLI entry point
│   └── test_cli.py      # Test CLI (no API keys required)
├── .env.example         # Example environment variables
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── setup.py             # Package installation
```

## Current Features

### Milestone 1: Environment Setup
- ✅ Virtual environment and dependency management
- ✅ Configuration and API key handling
- ✅ Logging setup
- ✅ Basic project structure

### Milestone 2: Command-Line Tool Framework
- ✅ Argument parsing and command handling
- ✅ Directory traversal for any codebase path
- ✅ File filtering by extension
- ✅ Project metadata extraction
- ✅ Code analysis for supported languages
- ✅ Test CLI for verification without API keys

### Milestone 3: Codebase Indexing
- ✅ Loading and chunking code files
- ✅ Generating embeddings with OpenAI
- ✅ Storing embeddings in Pinecone DB
- ✅ Namespace support for multiple codebases
- ✅ Index management (create, delete, stats)
- ✅ Batch processing for large codebases

### Milestone 4: RAG System and Agent Development
- ✅ Semantic code retrieval via embeddings
- ✅ Natural language querying of code
- ✅ Conversational interface with memory
- ✅ Code-specific prompt engineering
- ✅ Finding related code snippets
- ✅ Integration with Claude LLM for high-quality responses

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Troubleshooting

### Common Issues

1. **API key errors**: Make sure you have properly set up your .env file with valid API keys.

   ```bash
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   PINECONE_API_KEY=your-pinecone-api-key
   ```

2. **Package not found errors**: If you encounter errors about packages not being found, try reinstalling the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Model not found**: If you encounter errors about Claude models not being found, you can update the model name in `src/utils/config.py`:

   ```python
   # Try using a different model name if the current one isn't accessible
   LLM_MODEL = "claude-3-haiku-20240307"  # or another available model
   ```

4. **Rate limiting**: If you hit API rate limits, try reducing the batch size when indexing:

   ```bash
   codebase-indexer index --path /path/to/codebase --batch-size 50
   ```

5. **Import errors**: If you see "No module named 'utils'" or similar import errors after installation, this is a Python import path issue. Use one of these solutions:

   - Use the latest version (1.0.1+) which fixes the import issues
   - Install from the latest distribution:
     ```bash
     pip install --upgrade codebase-indexer
     ```
   - Or alternatively, use the direct runner script which includes import path fixes:
     ```bash
     # Download run-indexer.py
     curl -O https://raw.githubusercontent.com/yourusername/indexer/main/run-indexer.py
     python run-indexer.py configure
     ```

5. **Command not found**: If you get a "command not found" error after installing with pip:

   - Use our easy installer script (macOS/Linux):
     ```bash
     curl -O https://raw.githubusercontent.com/yourusername/indexer/main/easy-install.sh
     chmod +x easy-install.sh
     ./easy-install.sh
     ```

   - Check that the Python scripts directory is in your PATH:
     ```bash
     # Find where the script was installed
     pip show codebase-indexer
     
     # On macOS/Linux:
     find ~/Library/Python/*/bin ~/.local/bin -name "codebase-indexer*" 2>/dev/null
     
     # On Windows:
     dir %USERPROFILE%\AppData\Roaming\Python\*\Scripts\codebase-indexer*.exe
     
     # Add to your PATH:
     # macOS/Linux (add to your .bashrc, .zshrc, etc.)
     export PATH="$PATH:~/Library/Python/3.9/bin"  # Adjust the path as needed
     
     # Windows (in Command Prompt as Administrator)
     setx PATH "%PATH%;%USERPROFILE%\AppData\Roaming\Python\Python39\Scripts"
     ```

   - Try the alternate script names:
     ```bash
     indexer --help
     code-indexer --help
     ```

   - Install with `pip install --user` to ensure it installs in your user directory:
     ```bash
     pip install --user codebase-indexer
     ```

   - Run the package module directly if all else fails:
     ```bash
     # On macOS/Linux:
     python -m src.main
     
     # On Windows:
     python -m src.main
     ```
   
   - Use the direct runner script:
     ```bash
     # Download the runner script
     curl -O https://raw.githubusercontent.com/yourusername/indexer/main/run-indexer.py
     # Or clone the repo and use the script directly
     python run-indexer.py --help
     ```

For more help, please open an issue on GitHub.