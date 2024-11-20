#!/bin/bash

# Define the path to your virtual environment
VENV_PATH="./venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found at $VENV_PATH"
    echo "Creating venv"
    python -m venv $VENV_PATH
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

pip install -r requirements.txt

python main.py