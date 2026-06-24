from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QLineEdit,
    QPushButton,
    QComboBox,
    QHBoxLayout
)
from PySide6.QtCore import Qt

from frontend.widgets.validation_card import ValidationCard
from database.validation_repository import (
    get_validations,
    get_validations_by_operator_name
)

class HistoryWindow(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent_window = parent

        self.all_validations = []
        self.search_input = None
        self.status_filter = None
        self.cards_layout = None
        self.total_label = None

        self.setup_ui()
        self.reload_data()

    def setup_ui(self):
        self.setStyleSheet("background-color: #F4F6F8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(16)

        title = QLabel("Histórico de Validações")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #111827;
            border: none;
        """)

        subtitle = QLabel(
            "Acompanhe as validações realizadas e filtre por modelo, operador ou status."
        )
        subtitle.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            border: none;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.create_filters())

        self.total_label = QLabel()
        self.total_label.setStyleSheet("""
            font-size: 13px;
            font-weight: bold;
            color: #374151;
            border: none;
        """)

        layout.addWidget(self.total_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)

        content = QWidget()
        content.setStyleSheet("background-color: transparent;")

        self.cards_layout = QVBoxLayout(content)
        self.cards_layout.setSpacing(10)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setAlignment(Qt.AlignTop)

        scroll.setWidget(content)

        layout.addWidget(scroll, 1)

    def create_filters(self):
        panel = QFrame()

        panel.setFixedHeight(64)
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Buscar por modelo, tipo, operador ou data..."
        )
        self.search_input.setFixedHeight(44)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 0 12px;
                font-size: 13px;
                color: #111827;
            }

            QLineEdit:focus {
                border: 1px solid #8CC63F;
                background-color: #FFFFFF;
            }
        """)

        self.status_filter = QComboBox()
        self.status_filter.addItems(
            ["Todos", "CONFIRMADO", "DIVERGENTE", "PENDENTE"]
        )
        self.status_filter.setFixedHeight(44)
        self.status_filter.setFixedWidth(160)
        self.status_filter.setStyleSheet("""
            QComboBox {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 13px;
                color: #111827;
            }

            QComboBox:focus {
                border: 1px solid #8CC63F;
                background-color: #FFFFFF;
            }
        """)

        clear_button = QPushButton("Limpar")
        clear_button.setFixedHeight(40)
        clear_button.setFixedWidth(90)
        clear_button.setCursor(Qt.PointingHandCursor)
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #E5E7EB;
                color: #111827;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #D1D5DB;
            }
        """)

        self.search_input.textChanged.connect(self.render_cards)
        self.status_filter.currentTextChanged.connect(self.render_cards)
        clear_button.clicked.connect(self.clear_filters)

        layout.addWidget(self.search_input, 1)
        layout.addWidget(self.status_filter)
        layout.addWidget(clear_button)

        return panel

    def reload_data(self):
        if self.parent_window.user["role"] == "GESTOR":
            self.all_validations = get_validations()
        else:
            self.all_validations = get_validations_by_operator_name(
            self.parent_window.user["name"]
        )

        self.render_cards()

    def clear_filters(self):
        self.search_input.clear()
        self.status_filter.setCurrentIndex(0)
        self.render_cards()

    def get_filtered(self):
        search = self.search_input.text().strip().lower()
        status_filter = self.status_filter.currentText()

        filtered = []

        for validation in self.all_validations:
            status = str(validation[1])
            model = str(validation[2]).lower()
            meter_type = str(validation[3]).lower()
            operator = str(validation[4]).lower()
            created_at = str(validation[5]).lower()

            matches_search = (
                search == ""
                or search in model
                or search in meter_type
                or search in operator
                or search in created_at
            )

            matches_status = (
                status_filter == "Todos"
                or status == status_filter
            )

            if matches_search and matches_status:
                filtered.append(validation)

        return filtered

    def render_cards(self):
        if self.cards_layout is None:
            return

        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        validations = self.get_filtered()

        self.total_label.setText(
            f"Total: {len(validations)}"
        )

        if not validations:
            empty = QLabel("Nenhuma validação encontrada para os filtros selecionados.")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("""
                background-color: #FFFFFF;
                color: #6B7280;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
                padding: 30px;
                font-size: 14px;
            """)

            self.cards_layout.addWidget(empty)
            self.cards_layout.addStretch()
            return

        for validation in validations:
            card = ValidationCard(
                validation,
                self.parent_window.open_validation_details
            )

            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()