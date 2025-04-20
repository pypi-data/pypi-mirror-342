#!/bin/bash
# Easy installer for codebase-indexer that handles PATH issues

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
print_blue "    Codebase Indexer Easy Installer         "
print_blue "════════════════════════════════════════════"
echo ""

# Detect shell profile
detect_shell_profile() {
    if [ -n "$ZSH_VERSION" ]; then
        echo "$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "$HOME/.bash_profile"
        else
            echo "$HOME/.bashrc"
        fi
    else
        echo "$HOME/.profile"
    fi
}

SHELL_PROFILE=$(detect_shell_profile)
print_blue "Detected shell profile: $SHELL_PROFILE"

# Install the package
print_blue "Installing codebase-indexer..."
pip3 install --user codebase-indexer
print_green "✓ Package installed"

# Find the script location
PIP_SCRIPT_DIR=$(python -c "import site, os; print(os.path.join(site.USER_BASE, 'bin'))" 2>/dev/null || echo "$HOME/.local/bin")
print_blue "Script directory: $PIP_SCRIPT_DIR"

if [ -f "$PIP_SCRIPT_DIR/codebase-indexer" ]; then
    print_green "✓ Found codebase-indexer in $PIP_SCRIPT_DIR"
else
    print_yellow "⚠ Could not find codebase-indexer script in expected location"
    print_blue "Searching for script..."
    SCRIPT_PATH=$(find ~/Library/Python/*/bin ~/Library/Python/*/lib/python/bin ~/.local/bin -name "codebase-indexer*" 2>/dev/null | head -n 1)
    
    if [ -n "$SCRIPT_PATH" ]; then
        print_green "✓ Found script at: $SCRIPT_PATH"
        PIP_SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
    else
        print_yellow "⚠ Could not find the script. Will add common Python script directories to PATH"
        PIP_SCRIPT_DIR="$HOME/Library/Python/3.9/bin:$HOME/Library/Python/3.8/bin:$HOME/.local/bin"
    fi
fi

# Check if the script directory is in PATH
if [[ ":$PATH:" != *":$PIP_SCRIPT_DIR:"* ]]; then
    print_yellow "⚠ Script directory is not in your PATH"
    print_blue "Adding script directory to PATH in $SHELL_PROFILE..."
    
    # Add to shell profile
    echo "" >> "$SHELL_PROFILE"
    echo "# Added by codebase-indexer installer" >> "$SHELL_PROFILE"
    echo "export PATH=\"\$PATH:$PIP_SCRIPT_DIR\"" >> "$SHELL_PROFILE"
    
    print_green "✓ Added script directory to PATH"
    print_yellow "⚠ Please restart your terminal or run: source $SHELL_PROFILE"
else
    print_green "✓ Script directory is already in your PATH"
fi

# Create a local symbolic link as a fallback
if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    print_blue "Creating symbolic link in /usr/local/bin..."
    SCRIPT_PATH="$PIP_SCRIPT_DIR/codebase-indexer"
    if [ -f "$SCRIPT_PATH" ]; then
        ln -sf "$SCRIPT_PATH" /usr/local/bin/codebase-indexer 2>/dev/null || true
        print_green "✓ Created symbolic link: /usr/local/bin/codebase-indexer"
    fi
fi

print_blue "Verifying installation..."
if command -v codebase-indexer &>/dev/null; then
    print_green "✓ codebase-indexer command is available"
else
    print_yellow "⚠ Command not found in current session. Please restart your terminal"
    print_yellow "  or run: export PATH=\"\$PATH:$PIP_SCRIPT_DIR\""
fi

echo ""
print_green "════════════════════════════════════════════"
print_green "          Installation Complete!             "
print_green "════════════════════════════════════════════"
echo ""
print_blue "You can now use codebase-indexer with:"
echo ""
print_blue "1. Configure your API keys:"
echo "   codebase-indexer configure"
echo ""
print_blue "2. Index a codebase:"
echo "   codebase-indexer index --path /path/to/your/codebase"
echo ""
print_blue "If the command is still not found after restarting your terminal, try:"
echo "   $PIP_SCRIPT_DIR/codebase-indexer"
echo "   python -m src.main"
echo ""
print_yellow "For more help, see the troubleshooting section in the README."