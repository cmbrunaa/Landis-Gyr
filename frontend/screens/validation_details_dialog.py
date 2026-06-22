from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QWidget,
    QPushButton
)
from PySide6.QtCore import Qt

from database.validation_repository import get_validation_items


class ValidationDetailsDialog(QDialog):
    def __init__(self, validation):
        super().__init__()

        self.validation = validation

        self.setWindowTitle("Detalhes da Validação")
        self.setMinimumSize(900, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #F4F6F8;
            }

            QLabel {
                color: #111827;
                font-size: 14px;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(18)

        validation_id = validation[0]
        status = validation[1]
        meter_model = validation[2]
        meter_type = validation[3]
        operator_name = validation[4]
        created_at = validation[5]

        status_color = self.get_status_color(status)

        header_layout = QHBoxLayout()

        title_area = QVBoxLayout()
        title_area.setSpacing(4)

        title = QLabel(f"Validação #{validation_id}")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #111827;
            border: none;
        """)

        subtitle = QLabel("Detalhamento dos parâmetros analisados no XML.")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #6B7280;
            border: none;
        """)

        title_area.addWidget(title)
        title_area.addWidget(subtitle)

        status_label = QLabel(status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFixedHeight(32)
        status_label.setMinimumWidth(130)
        status_label.setStyleSheet(f"""
            background-color: {status_color}22;
            color: {status_color};
            border-radius: 16px;
            padding: 0 14px;
            font-size: 12px;
            font-weight: bold;
            border: none;
        """)

        header_layout.addLayout(title_area)
        header_layout.addStretch()
        header_layout.addWidget(status_label)

        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 14px;
                border: 1px solid #E1E5EA;
            }
        """)

        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(18, 16, 18, 16)
        info_layout.setSpacing(10)

        info_title = QLabel("Informações da Validação")
        info_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #111827;
            border: none;
        """)

        info_grid = QHBoxLayout()
        info_grid.setSpacing(10)

        info_grid.addWidget(self.create_info_box("Modelo", meter_model))
        info_grid.addWidget(self.create_info_box("Tipo", meter_type))
        info_grid.addWidget(self.create_info_box("Operador", operator_name))
        info_grid.addWidget(self.create_info_box("Data", created_at))

        info_layout.addWidget(info_title)
        info_layout.addLayout(info_grid)

        items_title = QLabel("Parâmetros analisados")
        items_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #111827;
            border: none;
        """)

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

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)

        items = get_validation_items(validation_id)

        if not items:
            empty_card = QFrame()
            empty_card.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border-radius: 14px;
                    border: 1px solid #E1E5EA;
                }
            """)

            empty_layout = QVBoxLayout(empty_card)
            empty_layout.setContentsMargins(18, 16, 18, 16)

            empty_label = QLabel(
                "Nenhum parâmetro detalhado foi salvo para esta validação.\n"
                "Faça uma nova validação para visualizar todos os itens analisados."
            )
            empty_label.setStyleSheet("""
                color: #6B7280;
                font-size: 14px;
                font-weight: bold;
                border: none;
            """)

            empty_layout.addWidget(empty_label)
            content_layout.addWidget(empty_card)

        else:
            for item in items:
                content_layout.addWidget(self.create_parameter_card(item))

        content_layout.addStretch()
        scroll.setWidget(content)

        close_button = QPushButton("Fechar")
        close_button.setFixedHeight(42)
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #8CC63F;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #79B832;
            }
        """)

        layout.addLayout(header_layout)
        layout.addWidget(info_card)
        layout.addWidget(items_title)
        layout.addWidget(scroll, 1)
        layout.addWidget(close_button)

    def get_status_color(self, status):
        if status == "DIVERGENTE":
            return "#DC2626"

        if status == "PENDENTE":
            return "#D97706"

        return "#16A34A"

    def create_info_box(self, title, value):
        box = QFrame()
        box.setMinimumHeight(70)
        box.setStyleSheet("""
            QFrame {
                background-color: #F9FAFB;
                border-radius: 10px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #6B7280;
            font-size: 12px;
            font-weight: bold;
            border: none;
        """)

        value_label = QLabel(str(value))
        value_label.setStyleSheet("""
            color: #111827;
            font-size: 13px;
            font-weight: bold;
            border: none;
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return box

    def create_parameter_card(self, item):
        parameter = item[0]
        expected = item[1]
        found = item[2]
        item_status = item[3]
        message = item[4]

        color = self.get_status_color(item_status)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E1E5EA;
                border-left: 5px solid {color};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        header = QHBoxLayout()

        parameter_label = QLabel(parameter)
        parameter_label.setStyleSheet("""
            color: #111827;
            font-size: 15px;
            font-weight: bold;
            border: none;
        """)

        status_label = QLabel(item_status)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFixedHeight(26)
        status_label.setMinimumWidth(110)
        status_label.setStyleSheet(f"""
            background-color: {color}22;
            color: {color};
            border-radius: 13px;
            padding: 0 10px;
            font-size: 11px;
            font-weight: bold;
            border: none;
        """)

        header.addWidget(parameter_label)
        header.addStretch()
        header.addWidget(status_label)

        details = QLabel(
            f"Esperado: {expected}\n"
            f"Encontrado: {found}\n"
            f"Mensagem: {message}"
        )
        details.setStyleSheet("""
            color: #374151;
            font-size: 13px;
            border: none;
        """)

        layout.addLayout(header)
        layout.addWidget(details)

        return card