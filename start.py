import os
from main import start, app

# Function to purge session files
def purge_sessions():
    print("Purging session files...")
    try:
        files_in_dir = os.listdir()  # Get all files in the current directory
        for file in files_in_dir:
            if file.endswith(".session") or file.endswith(".session-journal"):
                os.remove(file)
                print(f"Deleted: {file}")
    except Exception as e:
        print(f"Error purging session files: {e}")

# Purging session files and starting the bots
purge_sessions()
print("Starting Bots...")

# Clear terminal screen and run the bot
os.system('clear')  # Use 'cls' for Windows if needed
app.run(start())
