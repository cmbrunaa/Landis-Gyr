import sys
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "backend"))

from PySide6.QtWidgets import QApplication

from database.database import create_tables
from database.user_repository import create_user, find_user_by_username
from utils.password import hash_password

from frontend.screens.login_window import LoginWindow


def create_default_admin():
    admin = find_user_by_username("admin")

    if admin is None:
        create_user(
            name="Administrador",
            username="admin",
            password=hash_password("123"),
            role="GESTOR",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )


def main():
    create_tables()
    create_default_admin()

    app = QApplication(sys.argv)

    window = LoginWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()