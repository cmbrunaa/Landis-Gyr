from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PySide6.QtCore import Qt

from frontend.screens.validation_window import ValidationWindow
from frontend.screens.validation_details_dialog import ValidationDetailsDialog
from frontend.screens.history_window import HistoryWindow
from frontend.screens.reports_window import ReportsWindow
from frontend.screens.users_window import UsersWindow

from database.validation_repository import (
    get_dashboard_summary,
    get_validations,
    get_validations_by_operator,
)


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()

        self.user = user
        self.validation_window = None

        self.setWindowTitle("ValidaFlow")
        self.resize(1400, 800)

        container = QWidget()
        container.setStyleSheet("background-color: #F4F6F8;")

        root_layout = QHBoxLayout(container)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self.create_sidebar())
        root_layout.addWidget(self.create_main_area(), 1)

        self.setCentralWidget(container)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame { background-color: #151515; }

            QLabel {
                color: #FFFFFF;
                border: none;
            }

            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                text-align: left;
                padding: 15px 24px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #242424;
                color: #8CC63F;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 28, 0, 20)
        layout.setSpacing(4)

        logo = QLabel("ValidaFlow")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            color: #8CC63F;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 28px;
            border: none;
        """)

        dashboard_button = QPushButton("▣  Dashboard ")
        dashboard_button.clicked.connect(self.show_dashboard)

        btn_validate = QPushButton("✓  Validar XML")
        btn_validate.clicked.connect(self.open_validation)

        btn_history = QPushButton("☰  Histórico")
        btn_history.clicked.connect(self.show_history_screen)

        layout.addWidget(logo)
        layout.addWidget(dashboard_button)
        layout.addWidget(btn_validate)
        layout.addWidget(btn_history)

        if self.user["role"] == "GESTOR":

            btn_reports = QPushButton("⇩  Relatórios")
            btn_reports.clicked.connect(self.show_reports_screen)

            btn_users = QPushButton("+  Usuários")
            btn_users.clicked.connect(self.show_users_screen)

            layout.addWidget(btn_reports)
            layout.addWidget(btn_users)
        layout.addStretch()

        footer = QLabel("Projeto Integrador\nADS • UniOpet")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            color: #9A9A9A;
            font-size: 12px;
            margin-bottom: 10px;
            border: none;
        """)

        layout.addWidget(footer)

        return sidebar

    def create_main_area(self):
        area = QWidget()

        layout = QVBoxLayout(area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.create_topbar())
        layout.addWidget(self.create_dashboard_content(), 1)

        return area

    def create_topbar(self):
        topbar = QFrame()
        topbar.setFixedHeight(74)
        topbar.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E1E5EA;
            }
        """)

        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(30, 0, 30, 0)

        title = QLabel("ValidaFlow")
        title.setStyleSheet("""
            color: #222222;
            font-size: 19px;
            font-weight: bold;
            border: none;
        """)

        user_info = QLabel(f"{self.user['name']}  •  {self.user['role']}")
        user_info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        user_info.setStyleSheet("""
            color: #222222;
            font-size: 14px;
            font-weight: bold;
            border: none;
        """)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(user_info)

        return topbar

    def show_dashboard(self):
        self.replace_content(self.create_dashboard_content())

    def show_history_screen(self):
        self.replace_content(HistoryWindow(self))
        
    def show_reports_screen(self):
        self.replace_content(ReportsWindow(self))


    def show_users_screen(self):
        self.replace_content(UsersWindow(self))

    def create_dashboard_content(self):
        content = QWidget()
        content.setStyleSheet("background-color: #F4F6F8;")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(18)

        page_title = QLabel("Dashboard")
        page_title.setStyleSheet("""
            color: #111827;
            font-size: 30px;
            font-weight: bold;
            border: none;
        """)

        subtitle = QLabel("Resumo das validações First-Off realizadas no sistema.")
        subtitle.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            border: none;
        """)

        summary = get_dashboard_summary()

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(18)

        cards_layout.addWidget(self.create_card("Total de Validações", summary["total"], "▣"))
        cards_layout.addWidget(self.create_card("Confirmadas", summary["confirmed"], "✓"))
        cards_layout.addWidget(self.create_card("Divergentes", summary["divergent"], "✕"))
        cards_layout.addWidget(self.create_card("Pendentes", summary["pending"], "!"))

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(18)

        bottom_layout.addWidget(self.create_latest_validations_panel(), 2)
        bottom_layout.addWidget(self.create_operators_panel(), 1)

        layout.addWidget(page_title)
        layout.addWidget(subtitle)
        layout.addLayout(cards_layout)
        layout.addLayout(bottom_layout)
        layout.addStretch()

        return content

    def create_card(self, title, value, icon="▣"):
        card = QFrame()
        card.setFixedHeight(130)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E1E5EA;
            }

            QFrame:hover {
                background-color: #FBFCFD;
                border: 1px solid #C9D1DA;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        top_row = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            font-weight: bold;
            border: none;
        """)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(34, 34)
        icon_label.setStyleSheet("""
            background-color: #EAF6DC;
            color: #8CC63F;
            border-radius: 17px;
            font-size: 17px;
            font-weight: bold;
            border: none;
        """)

        value_label = QLabel(str(value))
        value_label.setStyleSheet("""
            color: #111827;
            font-size: 38px;
            font-weight: bold;
            border: none;
        """)

        top_row.addWidget(title_label)
        top_row.addStretch()
        top_row.addWidget(icon_label)

        layout.addLayout(top_row)
        layout.addStretch()
        layout.addWidget(value_label)

        return card

    def create_latest_validations_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E1E5EA;
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(16)

        title = QLabel("Últimas Validações")
        title.setStyleSheet("""
            color: #111827;
            font-size: 21px;
            font-weight: bold;
            border: none;
        """)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Status", "Modelo", "Operador", "Data"])

        validations = get_validations()[:6]
        table.setRowCount(len(validations))

        for row, item in enumerate(validations):
            values = [
                str(item[0]),
                str(item[1]),
                str(item[2]),
                str(item[4]),
                str(item[5]),
            ]

            for col, value in enumerate(values):
                cell = QTableWidgetItem(value)
                cell.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, col, cell)

        self.apply_table_style(table)

        layout.addWidget(title)
        layout.addWidget(table)

        return panel

    def create_operators_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E1E5EA;
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(16)

        title = QLabel("Validações por Operador")
        title.setStyleSheet("""
            color: #111827;
            font-size: 21px;
            font-weight: bold;
            border: none;
        """)

        layout.addWidget(title)

        operators = get_validations_by_operator()

        if not operators:
            empty = QLabel("Nenhuma validação registrada.")
            empty.setStyleSheet("""
                color: #666666;
                font-size: 14px;
                border: none;
            """)
            layout.addWidget(empty)
            layout.addStretch()
            return panel

        for operator_name, total in operators:
            row = QFrame()
            row.setStyleSheet("""
                QFrame {
                    background-color: #F9FAFB;
                    border-radius: 12px;
                    border: 1px solid #E5E7EB;
                }
            """)

            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(14, 12, 14, 12)

            name_label = QLabel(operator_name)
            name_label.setStyleSheet("""
                color: #111827;
                font-size: 14px;
                font-weight: bold;
                border: none;
            """)

            total_label = QLabel(str(total))
            total_label.setAlignment(Qt.AlignCenter)
            total_label.setFixedSize(32, 32)
            total_label.setStyleSheet("""
                background-color: #EAF6DC;
                color: #8CC63F;
                border-radius: 16px;
                font-size: 17px;
                font-weight: bold;
                border: none;
            """)

            row_layout.addWidget(name_label)
            row_layout.addStretch()
            row_layout.addWidget(total_label)

            layout.addWidget(row)

        layout.addStretch()

        return panel

    def apply_table_style(self, table):
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setShowGrid(False)
        table.setWordWrap(False)
        table.setFocusPolicy(Qt.NoFocus)

        for row in range(table.rowCount()):
            table.setRowHeight(row, 44)

        table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #FAFAFA;
                border: none;
                gridline-color: transparent;
                font-size: 13px;
                color: #111827;
            }

            QHeaderView::section {
                background-color: #F3F4F6;
                color: #374151;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }

            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #EEF0F2;
            }

            QTableWidget::item:selected {
                background-color: #EAF6DC;
                color: #111111;
            }
        """)

    def open_validation(self):
        self.validation_window = ValidationWindow(
            self.user,
            self.refresh_dashboard,
        )
        self.validation_window.show()

    def open_validation_details(self, validation):
        dialog = ValidationDetailsDialog(validation)
        dialog.exec()

    def refresh_dashboard(self):
        self.replace_content(self.create_dashboard_content())

    def replace_content(self, new_content):
        main_area = self.centralWidget().layout().itemAt(1).widget()
        main_layout = main_area.layout()

        old_content = main_layout.itemAt(1).widget()

        main_layout.removeWidget(old_content)
        old_content.deleteLater()

        main_layout.addWidget(new_content, 1)