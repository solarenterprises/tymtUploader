from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QFileDialog, QMessageBox
import os
import json
import shutil
import zipfile
import subprocess  # Import subprocess module
from PIL import Image  # Import PIL for image validation

class AddBrowserGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TymtUploader - Add Browser Game")
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

        # External URL
        self.external_url_input = QLineEdit()
        self.external_url_input.setPlaceholderText("Enter External URL")
        self.layout.addWidget(self.external_url_input)

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
        
        self.preview_image_path = ""
        self.asset_images = {}
        self.icon_image_path = ""

    def go_back_to_welcome(self):
        from menus.welcome_screen import WelcomeScreen
        self.welcome_screen = WelcomeScreen()
        self.welcome_screen.show()
        self.close()

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
        external_url = self.external_url_input.text()

        if not game_name or not publisher or not self.preview_image_path or len(self.asset_images) < 3 or not self.icon_image_path:
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
            "Category": ["Browser"],
            "ShortDescription": short_description,
            "Visible": True,
            "XRated": False,
            "GameFile": f"{game_folder}/game.json",
            "Preview": preview_image_dest,
            "Assets": f"{game_folder}/assets/*.webp",
            "Price": 0.00,
            "Blockchain": 3,
            "Type": "browser",
            "downloadType": "none",
            "Platform": 1,
            "isHyperPlayExclusive": False,
            "external_url": external_url
        }

        with open(os.path.join(game_folder, "game.json"), "w") as f:
            json.dump(game_json, f, indent=4)

        # Create index.json
        index_json = {
            "_id": game_id,
            "name": game_name,
            "short_description": short_description,
            "description": "Experience the game in your browser.",
            "tags": ["Browser", "Game"],
            "price": 0.00,
            "youtubeUrl": "https://youtubeurl",
            "platforms": {
                "browser": {
                    "name": game_name,
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
        QMessageBox.information(self, "Metadata Creation Complete", f"The zip file has been created: {zip_filename}")
        subprocess.run(["open", os.path.dirname(os.path.abspath(zip_filename))])