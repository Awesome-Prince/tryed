#!/bin/bash

# Killing any existing screen sessions
echo "Killing any existing screen sessions..."
pkill screen

# Pull the latest changes from the Git repository
echo "Pulling latest code from Git..."
git pull
clear

# Check if the 'manik' virtual environment exists, if not, create it
if [ ! -d "manik" ]; then
    echo "Creating virtual environment 'manik'..."
    python3 -m venv manik
else
    echo "Virtual environment 'manik' already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source manik/bin/activate
clear

# Start a new screen session and run the Python script in the background
echo "Starting the 'manik_session' in screen..."
screen -dmS manik_session
screen -S manik_session -X stuff 'python3 start.py\n'

echo "Setup complete. 'manik_session' is running."
