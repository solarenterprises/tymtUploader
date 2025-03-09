import subprocess
import transmissionrpc
from config import TRANSMISSION_HOST, TRANSMISSION_PORT

def create_torrent(game_folder, torrent_output):
    """ Create a torrent file using `transmission-create`. """
    TRACKERS = [
        "udp://tracker.tymt.com:1337/announce",
        "udp://tracker.tymt.com/announce",
        "http://tracker.tymt.com/announce",
        "udp://tracker2.tymt.com:1337/announce",
        "udp://tracker2.tymt.com/announce",
        "udp://tracker3.tymt.com:1337/announce",
        "udp://tracker3.tymt.com/announce"
    ]

    command = [
        "transmission-create",
        "-o", torrent_output,
        "-p",  # Public torrent
        "-t", ",".join(TRACKERS),  # Add trackers
        game_folder
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"✅ Torrent created: {torrent_output}")
        return torrent_output
    else:
        print(f"❌ Error creating torrent: {result.stderr}")
        return None

def seed_torrent(torrent_file):
    """ Start seeding using Transmission. """
    try:
        client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT)
        client.add_torrent(torrent_file)
        print(f"🚀 Seeding started for {torrent_file}")
    except Exception as e:
        print(f"❌ Error starting seeding: {e}")

def get_torrent_stats():
    """ Retrieve active torrent stats from Transmission. """
    try:
        client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT)
        torrents = client.get_torrents()
        stats = []
        for torrent in torrents:
            stat_entry = (
                f"🌍 {torrent.name} | ⬆ {torrent.uploadRatio:.2f} | Speed: {torrent.rateUpload / 1024:.2f} KB/s "
                f"| Peers: {torrent.peersConnected}"
            )
            stats.append(stat_entry)
        return stats
    except Exception as e:
        print(f"❌ Error retrieving torrent stats: {e}")
        return []

def delete_torrent(torrent_name):
    """ Delete a torrent using Transmission. """
    try:
        client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT)
        torrents = client.get_torrents()
        for torrent in torrents:
            if torrent_name in torrent.name:
                client.remove_torrent(torrent.id, delete_data=True)
                print(f"🗑️ Torrent {torrent_name} deleted.")
                return
        print(f"❌ Torrent {torrent_name} not found.")
    except Exception as e:
        print(f"❌ Error deleting torrent: {e}")

def check_torrent_integrity(torrent_file_path, folder_path):
    """ Check the integrity of the files being seeded using Transmission. """
    try:
        client = transmissionrpc.Client(TRANSMISSION_HOST, port=TRANSMISSION_PORT)
        torrents = client.get_torrents()
        for torrent in torrents:
            if torrent_file_path in torrent.name:
                torrent.verify()
                while torrent.status != 'seeding':
                    if torrent.status == 'checking':
                        continue
                    elif torrent.status == 'seeding':
                        return True
                    else:
                        return False
        return False
    except Exception as e:
        print(f"❌ Error checking torrent integrity: {e}")
        return False