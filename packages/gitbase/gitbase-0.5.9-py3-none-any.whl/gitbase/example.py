# GitBase v0.5.9 Showcase Example

from gitbase import MultiBase, PlayerDataSystem, DataSystem, NotificationManager, ProxyFile, is_online
from cryptography.fernet import Fernet
import sys

# -------------------------
# 1. Online Status Check
# -------------------------
print(f"Is Online: {is_online()}")  # Check if the system is online

# -------------------------
# 2. GitHub Database Setup
# -------------------------
GITHUB_TOKEN = "YOUR_TOKEN"
REPO_OWNER = "YOUR_GITHUB_USERNAME"
REPO_NAME = "YOUR_REPO_NAME"
encryption_key = Fernet.generate_key()  # Generate encryption key for secure storage

# MultiBase setup with fallback repository configurations (if needed)
database = MultiBase([
    {
        "token": GITHUB_TOKEN,
        "repo_owner": REPO_OWNER,
        "repo_name": REPO_NAME,
        "branch": "main"
    },
    # Additional GitBase configurations can be added here
    # {"token": "SECOND_TOKEN", "repo_owner": "SECOND_USERNAME", "repo_name": "SECOND_REPO", "branch": "main"}
])
# When using Legacy do the below instead
# from gitbase import GitBase
# database = GitBase(token=GITHUB_TOKEN, repo_owner=REPO_OWNER, repo_name=REPO_NAME)

# -------------------------
# 3. System Instantiation
# -------------------------
player_data_system = PlayerDataSystem(db=database, encryption_key=encryption_key)
data_system = DataSystem(db=database, encryption_key=encryption_key)

# -------------------------
# 4. File Upload & Download
# -------------------------
# Upload file to GitHub repository
database.upload_file(file_path="my_file.txt", remote_path="saved_files/my_file.txt")

# Download file from GitHub repository
database.download_file(remote_path="saved_files/my_file.txt", local_path="files/my_file.txt")

# -------------------------
# 5. File Streaming with ProxyFile
# -------------------------
proxy_file = ProxyFile(repo_owner=REPO_OWNER, repo_name=REPO_NAME, token=GITHUB_TOKEN, branch="main")

# Stream an audio file
audio_file = proxy_file.play_audio(remote_path="audio_files/sample_audio.wav")

# Stream a video file
video_file = proxy_file.play_video(remote_path="video_files/sample_video.mp4")

# -------------------------
# 6. Player Class Definition
# -------------------------
class Player:
    def __init__(self, username, score, password):
        self.username = username
        self.score = score
        self.password = password

# Create a sample player instance
player = Player(username="john_doe", score=100, password="123")

# -------------------------
# 7. Save & Load Player Data with Encryption
# -------------------------
# Save player data to the repository (with encryption)
player_data_system.save_account(
    username="john_doe",
    player_instance=player,
    encryption=True,
    attributes=["username", "score", "password"],
    path="players"
)

# Load player data
player_data_system.load_account(username="john_doe", player_instance=player, encryption=True)

# -------------------------
# 8. Game Flow Functions
# -------------------------
def load_game():
    print("Game starting...")

def main_menu():
    sys.exit("Exiting game...")

# -------------------------
# 9. Account Validation & Login
# -------------------------
# Validate player credentials
if player_data_system.get_all(path="players"):
    if player.password == input("Enter your password: "):
        print("Login successful!")
        load_game()
    else:
        print("Incorrect password!")
        main_menu()

# -------------------------
# 10. Save & Load General Data with Encryption
# -------------------------
# Save data (key-value) to the repository (with encryption)
data_system.save_data(key="key_name", value=69, path="data", encryption=True)

# Load and display specific key-value pair
loaded_key_value = data_system.load_data(key="key_name", path="data", encryption=True)
print(f"Key: {loaded_key_value.key}, Value: {loaded_key_value.value}")

# Display all stored data
print("All stored data:", data_system.get_all(path="data"))

# Delete specific key-value data
data_system.delete_data(key="key_name", path="data")

# -------------------------
# 11. Player Account Management
# -------------------------
# Display all player accounts
print("All player accounts:", player_data_system.get_all(path="players"))

# Delete a specific player account
NotificationManager.hide()  # Hide notifications temporarily
player_data_system.delete_account(username="john_doe")
NotificationManager.show()  # Show notifications again