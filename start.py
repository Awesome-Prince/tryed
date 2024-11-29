from main import start, app, app1
import os

# Function for purging session files
def purge_sessions():
    print("Purging session files...")
    for filename in os.listdir():
        if filename.endswith(".session") or filename.endswith(".session-journal"):
            os.remove(filename)

# Purge session files
purge_sessions()

print("Starting Bot1...")
os.system('clear')
app.run(start())

print("Starting Bot2...")
os.system('clear')
app1.run(start())
