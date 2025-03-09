from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QTextBrowser, QPushButton, QMessageBox
import socket
from config import TRANSMISSION_HOST, TRANSMISSION_PORT
from utils.torrent_utils import get_torrent_stats
from menus.game_submission import GameSubmission

class WelcomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TymtUploader - Welcome")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()

        # Welcome message
        self.welcome_label = QLabel("Welcome to TymtUploader!")
        self.layout.addWidget(self.welcome_label)
        
        # Dependency check
        self.requirements_browser = QTextBrowser()
        self.layout.addWidget(self.requirements_browser)
        
        # Check Port Button
        self.check_port_button = QPushButton("Check Dependencies")
        self.check_port_button.clicked.connect(self.check_dependencies)
        self.layout.addWidget(self.check_port_button)

        # Proceed button
        self.proceed_button = QPushButton("Proceed to Game Submission")
        self.proceed_button.clicked.connect(self.open_game_submission)
        self.layout.addWidget(self.proceed_button)

        # Seed Your Game button
        self.seed_game_button = QPushButton("Seed Your Game")
        self.seed_game_button.clicked.connect(self.open_seed_game)
        self.layout.addWidget(self.seed_game_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Initial check
        self.check_dependencies()

    def check_dependencies(self):
        dependencies = [
            "Checking dependencies...",
            "- Python Installed",
            "- PyQt6 Installed",
            "- Transmission Installed"
        ]

        # Check if ports are open
        ports = [1337, 51413]
        for port in ports:
            if is_port_open(TRANSMISSION_HOST, port):
                dependencies.append(f"- Port {port} is open for torrenting.")
            else:
                dependencies.append(f"- Port {port} is closed for torrenting.")

        # Check currently seeding torrents
        stats = get_torrent_stats()
        if stats:
            dependencies.append("You are currently seeding these torrents:")
            dependencies.extend(stats)
        else:
            dependencies.append("No torrents are currently seeding.")

        self.requirements_browser.setPlainText("\n".join(dependencies))

    def open_game_submission(self):
        self.game_submission_window = GameSubmission()
        self.game_submission_window.show()
        self.close()

    def open_seed_game(self):
        from menus.seed_game import SeedGame
        self.seed_game_window = SeedGame()
        self.seed_game_window.show()
        self.close()

def is_port_open(host, port):
    """ Check if a port is open on the given host. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # 1 second timeout
        result = sock.connect_ex((host, port))
        return result == 0