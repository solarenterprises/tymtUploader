import os
import json
import zipfile
import shutil
import subprocess
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from utils.torrent_utils import create_torrent, seed_torrent, check_torrent_integrity
from PIL import Image  # Import PIL for image validation

class AddNativeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TymtUploader - Add Native Game")
        self.setGeometry(200, 200, 600, 700)
        self.layout = QVBoxLayout()

        # Game Name
        self.game_name_input = QLineEdit()
        self.game_name_input.setPlaceholderText("Enter Game Name")
        self.layout.addWidget(self.game_name_input)
        
        # Publisher
        self.publisher_input = QLineEdit()
        self.publisher_input.setPlaceholderText("Enter Publisher")
        self.layout.addWidget(self.publisher_input)

        # Short Description
        self.short_description_input = QLineEdit()
        self.short_description_input.setPlaceholderText("Enter Short Description")
        self.layout.addWidget(self.short_description_input)

        # Executable Path
        self.executable_path_input = QLineEdit()
        self.executable_path_input.setPlaceholderText("Enter Executable Path")
        self.layout.addWidget(self.executable_path_input)

        # External URL
        self.external_url_input = QLineEdit()
        self.external_url_input.setPlaceholderText("Enter External URL")
        self.layout.addWidget(self.external_url_input)

        # Select Game Folder
        self.game_folder_dropdown = QComboBox()
        self.populate_game_folder_dropdown()
        self.game_folder_dropdown.currentIndexChanged.connect(self.update_game_folder_status)
        self.layout.addWidget(self.game_folder_dropdown)
        self.select_game_status = QLabel("❌")
        self.layout.addWidget(self.select_game_status)

        # Upload Preview Image
        self.upload_preview_button = QPushButton("Upload Preview Image")
        self.upload_preview_button.clicked.connect(self.upload_preview_image)
        self.layout.addWidget(self.upload_preview_button)
        self.upload_preview_status = QLabel("❌ Only .webp files supported. Maximum 100KB and 1600x900")
        self.layout.addWidget(self.upload_preview_status)

        # Upload Asset Images
        self.upload_asset1_button = QPushButton("Upload Asset Image 1")
        self.upload_asset1_button.clicked.connect(lambda: self.upload_asset_image(1))
        self.layout.addWidget(self.upload_asset1_button)
        self.upload_asset1_status = QLabel("❌ Only .webp files supported. Maximum 100KB and 1600x900")
        self.layout.addWidget(self.upload_asset1_status)

        self.upload_asset2_button = QPushButton("Upload Asset Image 2")
        self.upload_asset2_button.clicked.connect(lambda: self.upload_asset_image(2))
        self.layout.addWidget(self.upload_asset2_button)
        self.upload_asset2_status = QLabel("❌ Only .webp files supported. Maximum 100KB and 1600x900")
        self.layout.addWidget(self.upload_asset2_status)

        self.upload_asset3_button = QPushButton("Upload Asset Image 3")
        self.upload_asset3_button.clicked.connect(lambda: self.upload_asset_image(3))
        self.layout.addWidget(self.upload_asset3_button)
        self.upload_asset3_status = QLabel("❌ Only .webp files supported. Maximum 100KB and 1600x900")
        self.layout.addWidget(self.upload_asset3_status)

        # Upload Icon Image
        self.upload_icon_button = QPushButton("Upload Icon Image")
        self.upload_icon_button.clicked.connect(self.upload_icon_image)
        self.layout.addWidget(self.upload_icon_button)
        self.upload_icon_status = QLabel("❌ Only .webp files supported. Maximum 25KB and 512x512")
        self.layout.addWidget(self.upload_icon_status)

        # Proceed Button
        self.proceed_button = QPushButton("Create Game Metadata")
        self.proceed_button.clicked.connect(self.create_game_metadata)
        self.layout.addWidget(self.proceed_button)

        # Back to Welcome Screen button
        self.back_button = QPushButton("Back to Welcome Screen")
        self.back_button.clicked.connect(self.go_back_to_welcome)
        self.layout.addWidget(self.back_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        
        self.selected_game_folder = ""
        self.preview_image_path = ""
        self.asset_images = {}
        self.icon_image_path = ""

    def go_back_to_welcome(self):
        from menus.welcome_screen import WelcomeScreen
        self.welcome_screen = WelcomeScreen()
        self.welcome_screen.show()
        self.close()

    def populate_game_folder_dropdown(self):
        base_folder = "add-gamefolder-here"
        if os.path.exists(base_folder):
            folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
            self.game_folder_dropdown.addItems(folders)

    def update_game_folder_status(self):
        if self.game_folder_dropdown.currentText():
            self.select_game_status.setText("✅")
        else:
            self.select_game_status.setText("❌")

    def validate_image(self, file_path, max_size_kb, max_width, max_height):
        if not file_path.lower().endswith('.webp'):
            return False
        if os.path.getsize(file_path) > max_size_kb * 1024:
            return False
        with Image.open(file_path) as img:
            if img.width > max_width or img.height > max_height:
                return False
        return True

    def upload_preview_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Preview Image", "", "Image Files (*.webp)")
        if file_path and self.validate_image(file_path, 100, 1600, 900):
            self.preview_image_path = file_path
            self.upload_preview_status.setText("✅")
        else:
            self.upload_preview_status.setText("❌ Only .webp files supported. Maximum 100KB and 1600x900")

    def upload_asset_image(self, asset_number):
        file_path, _ = QFileDialog.getOpenFileName(self, f"Upload Asset Image {asset_number}", "", "Image Files (*.webp)")
        if file_path and self.validate_image(file_path, 100, 1600, 900):
            self.asset_images[asset_number] = file_path
            if asset_number == 1:
                self.upload_asset1_status.setText("✅")
            elif asset_number == 2:
                self.upload_asset2_status.setText("✅")
            elif asset_number == 3:
                self.upload_asset3_status.setText("✅")
        else:
            if asset_number == 1:
                self.upload_asset1_status.setText("❌ Only .webp files supported. Maximum 100KB and 1600x900")
            elif asset_number == 2:
                self.upload_asset2_status.setText("❌ Only .webp files supported. Maximum 100KB and 1600x900")
            elif asset_number == 3:
                self.upload_asset3_status.setText("❌ Only .webp files supported. Maximum 100KB and 1600x900")

    def upload_icon_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Icon Image", "", "Image Files (*.webp)")
        if file_path and self.validate_image(file_path, 25, 512, 512):
            self.icon_image_path = file_path
            self.upload_icon_status.setText("✅")
        else:
            self.upload_icon_status.setText("❌ Only .webp files supported. Maximum 25KB and 512x512")

    def create_game_metadata(self):
        game_name = self.game_name_input.text()
        publisher = self.publisher_input.text()
        short_description = self.short_description_input.text()
        executable_path = self.executable_path_input.text()
        external_url = self.external_url_input.text()
        selected_folder = self.game_folder_dropdown.currentText()
        self.selected_game_folder = os.path.join("add-gamefolder-here", selected_folder)

        if not game_name or not publisher or not self.selected_game_folder or not self.preview_image_path or len(self.asset_images) < 3 or not self.icon_image_path:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields and upload all required images.")
            return

        game_id = game_name.lower().replace(" ", "-")
        game_folder = os.path.join("gamesdb", publisher.lower().replace(" ", "-"), game_id)

        os.makedirs(game_folder, exist_ok=True)
        os.makedirs(os.path.join(game_folder, "assets"), exist_ok=True)

        # Copy images to the game folder
        preview_image_dest = os.path.join(game_folder, "preview.webp")
        shutil.copy(self.preview_image_path, preview_image_dest)

        for asset_number, asset_path in self.asset_images.items():
            asset_dest = os.path.join(game_folder, f"image{asset_number}.webp")
            shutil.copy(asset_path, asset_dest)

        icon_image_dest = os.path.join(game_folder, "icon.webp")
        shutil.copy(self.icon_image_path, icon_image_dest)

        # Create game.json
        game_json = {
            "GameID": game_id,
            "GameName": game_name,
            "Publisher": publisher,
            "Category": ["RPG", "First Shooter"],
            "ShortDescription": short_description,
            "Visible": True,
            "XRated": False,
            "GameFile": f"{game_folder}/game.json",
            "Preview": preview_image_dest,
            "Assets": f"{game_folder}/assets/*.webp",
            "Price": 0.00,
            "Blockchain": 3,
            "Type": "native",
            "downloadType": "torrent",
            "Platform": 1,
            "isHyperPlayExclusive": False,
            "external_url": ""
        }

        with open(os.path.join(game_folder, "game.json"), "w") as f:
            json.dump(game_json, f, indent=4)

        # Create index.json
        index_json = {
            "_id": game_id,
            "name": game_name,
            "short_description": short_description,
            "description": "Experience the iconic top-down view action with crime and chaos.",
            "tags": ["RPG", "Action", "Open-World"],
            "price": 0.00,
            "youtubeUrl": "https://youtubeurl",
            "platforms": {
                "windows_amd64": {
                    "name": game_name,
                    "executable": executable_path,
                    "installSize": "N/A",
                    "external_url": external_url
                }
            }
        }

        with open("index.json", "w") as f:
            json.dump(index_json, f, indent=4)

        # Create zip file
        os.makedirs("output/submission_packages", exist_ok=True)
        zip_filename = os.path.join("output/submission_packages", f"{game_id}.zip")
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write("index.json")
            for root, dirs, files in os.walk(game_folder):
                for file in files:
                    zipf.write(os.path.join(root, file))

        self.show_completion_message(zip_filename)

    def show_completion_message(self, zip_filename):
        reply = QMessageBox.question(self, "Metadata Creation Complete", "Game metadata and zip file created successfully. Would you like to seed this game now as a torrent?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.create_and_seed_torrent()
        else:
            QMessageBox.information(self, "Thank You", f"The zip file has been created: {zip_filename}")
            subprocess.run(["open", os.path.dirname(os.path.abspath(zip_filename))])

    def create_and_seed_torrent(self):
        os.makedirs("output/torrents", exist_ok=True)
        torrent_file_path = os.path.join("output/torrents", f"{os.path.basename(self.selected_game_folder)}.torrent")
        torrent_file = create_torrent(self.selected_game_folder, torrent_file_path)
        if torrent_file:
            seed_torrent(torrent_file)
            QMessageBox.information(self, "Seeding Started", "The game is now being seeded as a torrent.")
            self.show_torrent_manager(torrent_file_path)
        else:
            QMessageBox.warning(self, "Error", "Failed to create the torrent file.")

    def show_torrent_manager(self, torrent_file_path):
        manager = TorrentManager(torrent_file_path, self.selected_game_folder)
        manager.show()

class TorrentManager(QMainWindow):
    def __init__(self, torrent_file_path, folder_path):
        super().__init__()
        self.setWindowTitle("Torrent Manager")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()

        self.torrent_file_path = torrent_file_path
        self.folder_path = folder_path

        # Torrent file path
        self.torrent_file_label = QLabel(f"Torrent File: {self.torrent_file_path}")
        self.layout.addWidget(self.torrent_file_label)

        # Folder path
        self.folder_label = QLabel(f"Seeding Folder: {self.folder_path}")
        self.layout.addWidget(self.folder_label)

        # Check integrity button
        self.check_integrity_button = QPushButton("Check File Integrity")
        self.check_integrity_button.clicked.connect(self.check_file_integrity)
        self.layout.addWidget(self.check_integrity_button)

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def check_file_integrity(self):
        result = check_torrent_integrity(self.torrent_file_path, self.folder_path)
        if result:
            QMessageBox.information(self, "Integrity Check", "All files are intact.")
        else:
            QMessageBox.warning(self, "Integrity Check", "Some files are missing or corrupted.")