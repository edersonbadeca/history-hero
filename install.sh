#!/bin/bash

# Dotfiles Sync Installation Script
# This script installs dotfiles-sync globally so it's available system-wide

set -e

PYTHON_CMD=${PYTHON_CMD:-python3}
INSTALL_DIR="${HOME}/.local/bin"
BIN_SCRIPT="${INSTALL_DIR}/dotfiles-sync"

echo "🚀 Dotfiles Sync Installation"
echo "=============================="
echo ""

# Check if Python is installed
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Error: Python3 is not installed"
    exit 1
fi

echo "✓ Python found: $($PYTHON_CMD --version)"

# Create .local/bin directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Install the package
echo ""
echo "📦 Installing package..."
$PYTHON_CMD -m pip install --user -e . > /dev/null 2>&1
echo "✓ Package installed"

# Create wrapper script
echo "📝 Creating wrapper script..."
cat > "$BIN_SCRIPT" << 'EOF'
#!/bin/bash
python3 -m dotfiles_sync.cli "$@"
EOF

# Make it executable
chmod +x "$BIN_SCRIPT"
echo "✓ Wrapper script created at $BIN_SCRIPT"

# Add .local/bin to PATH if needed
SHELL_RC=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="${HOME}/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="${HOME}/.bashrc"
fi

if [[ -n "$SHELL_RC" ]]; then
    if grep -q "\.local/bin" "$SHELL_RC" 2>/dev/null; then
        echo "✓ PATH already configured"
    else
        echo "📝 Adding ~/.local/bin to PATH in $SHELL_RC"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        echo "✓ PATH updated"
    fi
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Reload your shell: source $SHELL_RC"
echo "2. Or restart your terminal"
echo ""
echo "Then start the daemon with:"
echo "  dotfiles-sync start --dot-file-path ~/dot-files"
echo ""

