#!/bin/bash
# Script to setup the codebase-indexer development environment

# Print colored status messages
print_green() {
    echo -e "\033[0;32m$1\033[0m"
}

print_yellow() {
    echo -e "\033[0;33m$1\033[0m"
}

print_red() {
    echo -e "\033[0;31m$1\033[0m"
}

print_blue() {
    echo -e "\033[0;34m$1\033[0m"
}

# Exit on error
set -e

print_blue "════════════════════════════════════════════"
print_blue "    Codebase Indexer Installation Script    "
print_blue "════════════════════════════════════════════"
echo ""

# Check Python version
if command -v python3 &>/dev/null; then
    python_version=$(python3 --version | awk '{print $2}')
    print_green "✓ Python $python_version detected"
else
    print_red "✗ Python 3 not found. Please install Python 3.8 or newer."
    exit 1
fi

# Check if pip is installed
if command -v pip3 &>/dev/null; then
    print_green "✓ pip detected"
else
    print_red "✗ pip not found. Please install pip."
    exit 1
fi

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_blue "Creating virtual environment..."
    python3 -m venv venv
    
    if [ ! -d "venv" ]; then
        print_red "✗ Failed to create virtual environment. Please install venv package."
        print_yellow "Try: pip3 install virtualenv"
        exit 1
    fi
    
    print_green "✓ Virtual environment created successfully"
else
    print_green "✓ Virtual environment already exists"
fi

# Activate virtual environment
print_blue "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_green "✓ Virtual environment activated"
else
    print_red "✗ Activation script not found. Virtual environment may be corrupt."
    print_yellow "Try deleting the venv directory and running this script again."
    exit 1
fi

# Upgrade pip
print_blue "Upgrading pip..."
pip install --upgrade pip
print_green "✓ pip upgraded"

# Install dependencies
print_blue "Installing dependencies..."
pip install -r requirements.txt
print_green "✓ Dependencies installed"

# Install the package in development mode
print_blue "Installing package in development mode..."
pip install -e .
print_green "✓ Package installed in development mode"

# Create logs directory
print_blue "Creating logs directory..."
mkdir -p logs
print_green "✓ Logs directory created"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_blue "Creating .env file from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_green "✓ .env file created from example"
        print_yellow "⚠ Please edit the .env file with your API keys."
    else
        print_yellow "⚠ .env.example not found, creating empty .env file"
        touch .env
        echo "OPENAI_API_KEY=" >> .env
        echo "ANTHROPIC_API_KEY=" >> .env
        echo "PINECONE_API_KEY=" >> .env
        print_yellow "⚠ Please edit the .env file with your API keys."
    fi
else
    print_green "✓ .env file already exists"
fi

# Verify setup
print_blue "Verifying setup..."
python src/verify_setup.py

# Install CLI tool globally (optional)
print_blue "Would you like to install the CLI tool globally? (y/N)"
read -r install_globally

if [[ $install_globally =~ ^[Yy]$ ]]; then
    print_blue "Installing CLI tool globally..."
    pip install .
    print_green "✓ CLI tool installed globally"
    print_yellow "You can now use 'codebase-indexer' or 'indexer' from anywhere"
fi

echo ""
print_green "════════════════════════════════════════════"
print_green "          Setup Complete! Next Steps:        "
print_green "════════════════════════════════════════════"
echo ""
print_blue "1. Configure your API keys using the interactive setup:"
echo "   codebase-indexer configure"
echo ""
print_blue "   You'll need API keys from:"
echo "   - OpenAI (https://platform.openai.com/)"
echo "   - Anthropic (https://www.anthropic.com/)"
echo "   - Pinecone (https://www.pinecone.io/)"
echo ""
print_blue "2. Activate the virtual environment when needed:"
echo "   source venv/bin/activate"
echo ""
print_blue "3. Start using the tool:"
echo "   codebase-indexer --help"
echo ""
print_blue "4. Index a codebase:"
echo "   codebase-indexer index --path /path/to/your/codebase"
echo ""
print_blue "5. Query your indexed codebase:"
echo "   codebase-indexer query --query \"How does file loading work?\""
echo ""
print_yellow "For more information, refer to the README.md file."