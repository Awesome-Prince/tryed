from main import start, app
import os

def purge_session_files():
    """
    Function to purge session files.
    """
    print("Purging session files...")
    for filename in os.listdir():
        if filename.endswith(".session") or filename.endswith(".session-journal"):
            os.remove(filename)

# Purge old session files
purge_session_files()

print("Starting Bots...")
os.system('clear')

# Run the app with the start function
app.run(start())