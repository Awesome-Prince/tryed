# Pull the latest changes from the Git repository
git pull

# Clear the terminal to keep things clean
clear

# Check if the "manik" directory (for the virtual environment) doesn't exist
# If it doesn't exist, create a new virtual environment
if [ ! -d "manik" ]; then
    python3 -m venv manik
fi

# Activate the virtual environment
source manik/bin/activate

# Clear the terminal again after activating the virtual environment
clear

# Start the Python application by running start.py
python3 start.py
