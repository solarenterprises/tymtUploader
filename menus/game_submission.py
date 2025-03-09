from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from menus.add_native import AddNativeGame
from menus.add_browser import AddBrowserGame

class GameSubmission(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TymtUploader - Game Submission")
        self.setGeometry(200, 200, 600, 400)
        self.layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("Select game type")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Spacer
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Game submission menu
        self.menu = QComboBox()
        self.menu.addItems([
            "Native Game",
            "Browser Game"
        ])
        self.layout.addWidget(self.menu)

        # Spacer
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Proceed button
        self.proceed_button = QPushButton("Proceed")
        self.proceed_button.clicked.connect(self.open_selected_menu)
        self.layout.addWidget(self.proceed_button)
        
        # Back to Welcome Screen button
        self.back_button = QPushButton("Back to Welcome Screen")
        self.back_button.clicked.connect(self.go_back_to_welcome)
        self.layout.addWidget(self.back_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_selected_menu(self):
        selected_option = self.menu.currentText()

        if selected_option == "Native Game":
            self.new_window = AddNativeGame()
        elif selected_option == "Browser Game":
            self.new_window = AddBrowserGame()

        self.new_window.show()
        self.close()
    
    def go_back_to_welcome(self):
        from menus.welcome_screen import WelcomeScreen
        self.welcome_screen = WelcomeScreen()
        self.welcome_screen.show()
        self.close()