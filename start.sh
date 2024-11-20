#!/bin/bash

# Define the path to your virtual environment
VENV_PATH="./venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found at $VENV_PATH"
    echo "Creating venv"
    python -m venv $VENV_PATH

    sqlite3 reports.db < create_db.sql

fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

echo "Checking and installing librairies"
pip install -r requirements.txt

echo "Launching the bot"
python main.py