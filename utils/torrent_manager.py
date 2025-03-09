from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QInputDialog
from utils.torrent_utils import seed_torrent, get_torrent_stats, delete_torrent

class SeedGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TymtUploader - Seed Your Game")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()

        # Add Torrent Button
        self.add_torrent_button = QPushButton("Add Torrent to Seed")
        self.add_torrent_button.clicked.connect(self.add_torrent)
        self.layout.addWidget(self.add_torrent_button)

        # View Torrent Stats Button
        self.view_torrents_button = QPushButton("View Torrent Stats")
        self.view_torrents_button.clicked.connect(self.view_torrent_stats)
        self.layout.addWidget(self.view_torrents_button)

        # Delete Torrent Button
        self.delete_torrent_button = QPushButton("Delete Torrent")
        self.delete_torrent_button.clicked.connect(self.delete_torrent)
        self.layout.addWidget(self.delete_torrent_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Back to Welcome Screen button
        self.back_button = QPushButton("Back to Welcome Screen")
        self.back_button.clicked.connect(self.go_back_to_welcome)
        self.layout.addWidget(self.back_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
    
    def add_torrent(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Torrent File", "", "Torrent Files (*.torrent)")
        if file_path:
            seed_torrent(file_path)
    
    def view_torrent_stats(self):
        stats = get_torrent_stats()
        stats_message = "\n".join(stats)
        QMessageBox.information(self, "Torrent Stats", stats_message)
    
    def delete_torrent(self):
        stats = get_torrent_stats()
        torrent_names = [stat.split(" | ")[0][2:] for stat in stats]  # Extract torrent names from stats
        if not torrent_names:
            QMessageBox.information(self, "No Torrents", "No torrents are currently seeding.")
            return
        
        torrent_name, ok = QInputDialog.getItem(self, "Select Torrent to Delete", "Torrent:", torrent_names, 0, False)
        if ok and torrent_name:
            delete_torrent(torrent_name)
            QMessageBox.information(self, "Torrent Deleted", f"Torrent {torrent_name} has been deleted.")
        
    def go_back_to_welcome(self):
        from menus.welcome_screen import WelcomeScreen
        self.welcome_screen = WelcomeScreen()
        self.welcome_screen.show()
        self.close()