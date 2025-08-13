#!/bin/bash
# Script to use Quarto with the uv-managed Python environment

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the project directory
cd "$SCRIPT_DIR"

# Activate the virtual environment
source .venv/bin/activate

# Execute the command passed as arguments
exec "$@"
