from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QFrame
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from services.auth_service import login
from frontend.core.paths import LOGO_PATH, BACKGROUND_PATH
from frontend.styles.theme import LOGIN_STYLE
from frontend.screens.main_window import MainWindow

class ImagePanel(QLabel):
    def __init__(self, image_path):
        super().__init__()

        self.original_pixmap = QPixmap(str(image_path))
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(600)

    def resizeEvent(self, event):
        if not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            self.setPixmap(scaled_pixmap)

        super().resizeEvent(event)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - First-Off Automatiza Landis+Gyr")
        self.resize(1400, 800)
        self.setStyleSheet(LOGIN_STYLE)
        self.main_window = None
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        left_image = ImagePanel(BACKGROUND_PATH)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(90, 40, 90, 40)

        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)

        logo_pixmap = QPixmap(str(LOGO_PATH))
        logo.setPixmap(
            logo_pixmap.scaled(
                300,
                140,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        title = QLabel("Sistema de Validação Automática")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        subtitle = QLabel("First-Off Landis+Gyr")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 15px; color: #666666;")

        user_label = QLabel("Usuário")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Digite seu usuário")

        password_label = QLabel("Senha")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("ENTRAR")
        login_button.clicked.connect(self.handle_login)

        user_label.setFixedWidth(380)
        password_label.setFixedWidth(380)
        self.username_input.setFixedWidth(450)
        self.password_input.setFixedWidth(450)
        login_button.setFixedWidth(450)

        footer = QLabel("Projeto Integrador Extensionista • ADS • UniOpet")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 12px; color: #666666;")

        right_layout.addWidget(logo)
        right_layout.addSpacing(20)
        right_layout.addWidget(title)
        right_layout.addWidget(subtitle)
        right_layout.addSpacing(35)
        right_layout.addWidget(user_label)
        right_layout.addWidget(self.username_input)
        right_layout.addSpacing(15)
        right_layout.addWidget(password_label)
        right_layout.addWidget(self.password_input)
        right_layout.addSpacing(25)
        right_layout.addWidget(login_button)
        right_layout.addSpacing(40)
        right_layout.addWidget(footer)

        main_layout.addWidget(left_image, 2)
        main_layout.addWidget(right_panel, 3)

    def handle_login(self):
        username = self.username_input.text().strip().lower()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Atenção", "Informe usuário e senha.")
            return

        user = login(username, password)

        if user is None:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")
            return

        self.main_window = MainWindow(user)
        self.main_window.showMaximized()
        self.close()    
