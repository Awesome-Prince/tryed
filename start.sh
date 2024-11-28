#!/bin/bash

# Terminate any running screen sessions
pkill screen

# Pull latest updates from Git
git pull

# Clear the terminal
clear

# Create virtual environment if it doesn't exist
if [ ! -d "manik" ]; then
    python3 -m venv manik
fi

# Activate the virtual environment
source manik/bin/activate

# Clear the terminal again after activation
clear

# Start a new screen session for the bot
screen -dmS manik_session
screen -S manik_session -X stuff 'python3 start.py\n'
