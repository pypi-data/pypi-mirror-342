#!/bin/bash
set -euo pipefail

# Determine the directory of this script and cd to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_message() {
    echo -e "${GREEN}==>${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}WARNING:${NC} $1"
}

print_error() {
    echo -e "${RED}ERROR:${NC} $1"
}

# --- VERSION parsing ---
VERSION="${VERSION:-}"
if [[ ${1:-} == --version ]]; then
    VERSION="${2:-}" || print_error "--version flag given but no value"
fi

# Check if virtual environment is activated
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
    print_warning "Virtual environment not activated. It's recommended to use a virtual environment."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for required tools
if ! command -v python3 &> /dev/null; then
    print_error "python3 is required but not installed."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    print_error "pip is required but not installed."
    exit 1
fi

if ! command -v git &> /dev/null; then
    print_error "git is required but not installed."
    exit 1
fi

# Install required build tools if not present
print_message "Checking/Installing build requirements..."
pip install --quiet build twine setuptools_scm

# Clean previous builds
print_message "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# --- Version handling for setuptools_scm ---
if [[ -z "$VERSION" ]]; then
    print_message "Checking current version from git tags (setuptools_scm)..."
    current_version=$(git describe --tags --abbrev=0 2>/dev/null || echo "0.0.0")
    IFS=. read -r major minor patch <<< "${current_version#v}"
    VERSION="$major.$minor.$((patch+1))"
    print_message "No VERSION supplied → using next patch: $VERSION"
else
    print_message "Using explicit VERSION: $VERSION"
fi

# Offer to create matching Git tag (optional)
read -rp "Create Git tag v$VERSION (y/N)? " reply
echo
if [[ $reply =~ ^[Yy]$ ]]; then
    git tag "v$VERSION" && git push origin "v$VERSION"
fi

# Export pretend version for setuptools‑scm
export SETUPTOOLS_SCM_PRETEND_VERSION="$VERSION"

# Build package
print_message "Building package..."
if ! python3 -m build; then
    print_error "Build failed!"
    exit 1
fi

# Verify .pypirc exists
if [ ! -f ~/.pypirc ]; then
    print_error ".pypirc file not found in home directory!"
    print_message "Please create ~/.pypirc with your PyPI token first."
    exit 1
fi

# Upload to PyPI
print_message "Uploading to PyPI..."
if ! python3 -m twine upload dist/*; then
    print_error "Upload failed!"
    exit 1
fi

print_message "Package $VERSION published 🎉" 