#!/bin/bash
set -e

echo "Setting up music-stem-separator project environment"
echo "=================================================="

# Check if Python 3.12 is installed
if ! command -v python3.12 &> /dev/null; then
    echo "Python 3.12 is required but not found"
    echo "Please install Python 3.12 with homebrew:"
    echo "brew install python@3.12"
    exit 1
fi

# Make sure we're in the project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Install UV if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing UV package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.cargo/env"
fi

# Remove existing venv if it exists
if [ -d ".venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf .venv
fi

# Create a new virtual environment with Python 3.12
echo "Creating new virtual environment with Python 3.12..."
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install base dependencies with uv
echo "Installing base dependencies with UV..."
uv pip install -e ".[dev]"

# Install chromaprint (for audiofingerprinting)
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Please install homebrew first."
    exit 1
fi

if ! brew list chromaprint &> /dev/null; then
    echo "Installing chromaprint for audio fingerprinting..."
    brew install chromaprint
fi

# Ask if the user wants to install optional dependencies
read -p "Do you want to try installing optional dependencies (aubio, madmom)? These may require additional setup (y/n): " install_optional

if [[ $install_optional == "y" || $install_optional == "Y" ]]; then
    echo "Attempting to install optional dependencies..."
    uv pip install -e ".[extra]" || {
        echo "Some optional dependencies failed to install."
        echo "You can still use the core functionality without them."
        echo "To install them manually later, run: uv pip install -e \".[extra]\""
    }
else
    echo "Skipping optional dependencies."
    echo "To install them later, run: uv pip install -e \".[extra]\""
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "    source .venv/bin/activate"
echo ""
echo "To deactivate the virtual environment, run:"
echo "    deactivate"
echo ""
echo "To run the analyse command:"
echo "    analyse [input_dir] [options]"
echo ""
echo "To run the split command:"
echo "    split [input_dir] [options]"
echo "" 