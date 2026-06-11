from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QMessageBox,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog
)
from PySide6.QtCore import Qt

from database.user_repository import (
    create_user,
    find_user_by_username,
    get_users
)
from utils.password import hash_password


class UserFormDialog(QDialog):
    def __init__(self, refresh_callback):
        super().__init__()

        self.refresh_callback = refresh_callback

        self.setWindowTitle("Cadastrar Usuário")
        self.setFixedSize(460, 430)
        self.setStyleSheet("background-color: #F4F6F8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Novo Usuário")
        title.setStyleSheet("""
            color: #111827;
            font-size: 24px;
            font-weight: bold;
        """)

        self.name_input = self.create_input("Nome completo")
        self.username_input = self.create_input("Usuário")
        self.password_input = self.create_input("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.role_input = QComboBox()
        self.role_input.addItems(["OPERADOR", "GESTOR"])
        self.role_input.setFixedHeight(40)
        self.role_input.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 13px;
            }
        """)

        buttons = QHBoxLayout()

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.close)

        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.save_user)

        for button in [cancel_button, save_button]:
            button.setFixedHeight(40)
            button.setCursor(Qt.PointingHandCursor)

        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #E5E7EB;
                color: #111827;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
        """)

        save_button.setStyleSheet("""
            QPushButton {
                background-color: #8CC63F;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #79B832;
            }
        """)

        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(self.create_label("Nome"))
        layout.addWidget(self.name_input)
        layout.addWidget(self.create_label("Usuário"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.create_label("Senha"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.create_label("Perfil"))
        layout.addWidget(self.role_input)
        layout.addStretch()
        layout.addLayout(buttons)

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            color: #374151;
            font-size: 13px;
            font-weight: bold;
        """)
        return label

    def create_input(self, placeholder):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedHeight(40)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 13px;
            }

            QLineEdit:focus {
                border: 1px solid #8CC63F;
            }
        """)
        return input_field

    def save_user(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip().lower()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not name or not username or not password:
            QMessageBox.warning(
                self,
                "Campos obrigatórios",
                "Preencha nome, usuário e senha."
            )
            return

        existing_user = find_user_by_username(username)

        if existing_user is not None:
            QMessageBox.warning(
                self,
                "Usuário já existe",
                "Já existe um usuário cadastrado com esse nome de usuário."
            )
            return

        create_user(
            name=name,
            username=username,
            password=hash_password(password),
            role=role,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        QMessageBox.information(
            self,
            "Usuário cadastrado",
            "Usuário cadastrado com sucesso."
        )

        self.refresh_callback()
        self.close()


class UsersWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent_window = parent
        self.setStyleSheet("background-color: #F4F6F8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(18)

        header = QHBoxLayout()

        title_area = QVBoxLayout()

        title = QLabel("Usuários")
        title.setStyleSheet("""
            color: #111827;
            font-size: 30px;
            font-weight: bold;
            border: none;
        """)

        subtitle = QLabel("Gerencie operadores e gestores autorizados a acessar o sistema.")
        subtitle.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            border: none;
        """)

        title_area.addWidget(title)
        title_area.addWidget(subtitle)

        new_user_button = QPushButton("+ Novo Usuário")
        new_user_button.setFixedHeight(42)
        new_user_button.setCursor(Qt.PointingHandCursor)
        new_user_button.clicked.connect(self.open_user_form)
        new_user_button.setStyleSheet("""
            QPushButton {
                background-color: #8CC63F;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0 18px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #79B832;
            }
        """)

        header.addLayout(title_area)
        header.addStretch()
        header.addWidget(new_user_button)

        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E1E5EA;
            }
        """)

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 22, 24, 24)
        panel_layout.setSpacing(14)

        filters = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome ou usuário...")
        self.search_input.setFixedHeight(40)

        self.role_filter = QComboBox()
        self.role_filter.addItems(["Todos", "OPERADOR", "GESTOR"])
        self.role_filter.setFixedHeight(40)

        clear_button = QPushButton("Limpar")
        clear_button.setFixedHeight(40)

        self.search_input.textChanged.connect(self.load_users_table)
        self.role_filter.currentTextChanged.connect(self.load_users_table)
        clear_button.clicked.connect(self.clear_filters)

        for field in [self.search_input, self.role_filter]:
            field.setStyleSheet("""
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 13px;
            """)

        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #E5E7EB;
                color: #111827;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
        """)

        filters.addWidget(self.search_input, 2)
        filters.addWidget(self.role_filter, 1)
        filters.addWidget(clear_button)

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)
        self.users_table.setHorizontalHeaderLabels([
            "ID",
            "Nome",
            "Usuário",
            "Perfil"
        ])

        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.verticalHeader().setVisible(False)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                border: none;
                gridline-color: #E5E7EB;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #111111;
                color: #FFFFFF;
                padding: 10px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 8px;
            }
        """)

        self.total_label = QLabel()
        self.total_label.setStyleSheet("""
            color: #374151;
            font-size: 13px;
            font-weight: bold;
        """)

        panel_layout.addLayout(filters)
        panel_layout.addWidget(self.users_table)
        panel_layout.addWidget(self.total_label)

        layout.addLayout(header)
        layout.addWidget(panel)
        layout.addStretch()

        self.load_users_table()

    def open_user_form(self):
        dialog = UserFormDialog(self.load_users_table)
        dialog.exec()

    def clear_filters(self):
        self.search_input.clear()
        self.role_filter.setCurrentIndex(0)
        self.load_users_table()

    def load_users_table(self):
        users = get_users()

        search = self.search_input.text().strip().lower()
        role = self.role_filter.currentText()

        filtered_users = []

        for user in users:
            user_id = user[0]
            name = str(user[1])
            username = str(user[2])
            user_role = str(user[3])

            matches_search = (
                search == ""
                or search in name.lower()
                or search in username.lower()
            )

            matches_role = (
                role == "Todos"
                or user_role == role
            )

            if matches_search and matches_role:
                filtered_users.append(user)

        self.users_table.setRowCount(len(filtered_users))

        for row, user in enumerate(filtered_users):
            for col, value in enumerate(user):
                self.users_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(str(value))
                )

        self.total_label.setText(
            f"Total de usuários: {len(filtered_users)}"
        )