import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTextBrowser, QPushButton
from qt_material import apply_stylesheet
from menus.welcome_screen import WelcomeScreen


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply Material Theme
    apply_stylesheet(app, theme='dark_teal.xml')  # Options: 'dark_blue.xml', 'light_purple.xml', etc.
    
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec())

class WelcomeScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TymtUploader - Welcome")
        self.setGeometry(200, 200, 800, 600)  # Increased window size
        self.layout = QVBoxLayout()

        # Welcome message
        self.welcome_label = QLabel("Welcome to TymtUploader!")
        self.layout.addWidget(self.welcome_label)
        
        # Dependency check
        self.requirements_browser = QTextBrowser()
        self.requirements_browser.setPlainText("Checking dependencies...\n- Python Installed\n- PyQt6 Installed\n- Transmission Installed")
        self.layout.addWidget(self.requirements_browser)

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

    def open_game_submission(self):
        from menus.game_submission import GameSubmission
        self.game_submission_window = GameSubmission()
        self.game_submission_window.show()
        self.close()

    def open_seed_game(self):
        from menus.seed_game import SeedGame
        self.seed_game_window = SeedGame()
        self.seed_game_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec())