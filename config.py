import os

# Paths
TORRENT_DIR = os.path.join(os.getcwd(), "output", "torrents")
SUBMISSION_DIR = os.path.join(os.getcwd(), "output", "submission_packages")

# Ensure directories exist
os.makedirs(TORRENT_DIR, exist_ok=True)
os.makedirs(SUBMISSION_DIR, exist_ok=True)

# Transmission settings
TRANSMISSION_HOST = 'localhost'  # or the appropriate host
TRANSMISSION_PORT = 9091  # or the appropriate port


# GitHub Repo (adjust if needed)
GITHUB_RAW_URL = "https://raw.githubusercontent.com/solarenterprises/tymtdb/main/index.json"