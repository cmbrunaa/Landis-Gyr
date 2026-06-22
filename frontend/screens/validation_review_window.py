from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea
)
from PySide6.QtCore import Qt

from database.validation_repository import (
    save_validation,
    save_divergences,
    save_validation_items
)


class ValidationReviewWindow(QWidget):

    def __init__(self, user, validation, xml_data, refresh_callback):
        super().__init__()

        self.user = user
        self.validation = validation
        self.xml_data = xml_data
        self.refresh_callback = refresh_callback

        self.setWindowTitle("Revisão da Validação")
        self.resize(900, 700)
        self.setStyleSheet("background-color: #F4F6F8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(18)

        title = QLabel("Revisão da Validação")
        title.setStyleSheet("""
            color: #111827;
            font-size: 28px;
            font-weight: bold;
            border: none;
        """)

        subtitle = QLabel(
            "Confira os parâmetros analisados antes de finalizar a validação."
        )
        subtitle.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            border: none;
        """)

        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(14)

        summary_layout.addWidget(
            self.create_summary_card("Confirmados", self.validation["confirmed"], "#16A34A")
        )
        summary_layout.addWidget(
            self.create_summary_card("Pendentes", self.validation["pending"], "#D97706")
        )
        summary_layout.addWidget(
            self.create_summary_card("Divergentes", self.validation["divergent"], "#DC2626")
        )
        summary_layout.addWidget(
            self.create_summary_card("Conformidade", f"{self.validation['conformity']}%", "#8CC63F")
        )

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

        self.items_layout = QVBoxLayout(content)
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_layout.setSpacing(10)

        for item in self.validation["results"]:
            self.items_layout.addWidget(self.create_item_card(item))

        self.items_layout.addStretch()
        scroll.setWidget(content)

        save_btn = QPushButton("Finalizar Validação")
        save_btn.setFixedHeight(44)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.finish)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #8CC63F;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #79B832;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(summary_layout)
        layout.addWidget(scroll, 1)
        layout.addWidget(save_btn)

    def create_summary_card(self, title, value, color):
        card = QFrame()
        card.setFixedHeight(95)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 14px;
                border: 1px solid #E1E5EA;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #6B7280;
            font-size: 13px;
            font-weight: bold;
            border: none;
        """)

        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 28px;
            font-weight: bold;
            border: none;
        """)

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)

        return card

    def create_item_card(self, item):
        status = item["status"]

        color = "#16A34A"
        if status == "DIVERGENTE":
            color = "#DC2626"
        elif status == "PENDENTE":
            color = "#D97706"

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
        layout.setSpacing(6)

        top_row = QHBoxLayout()

        parameter_label = QLabel(item["parameter"])
        parameter_label.setStyleSheet("""
            color: #111827;
            font-size: 15px;
            font-weight: bold;
            border: none;
        """)

        status_label = QLabel(status)
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

        top_row.addWidget(parameter_label)
        top_row.addStretch()
        top_row.addWidget(status_label)

        details = QLabel(
            f"Esperado: {item['expected']}\n"
            f"Encontrado: {item['found']}\n"
            f"Mensagem: {item['message']}"
        )
        details.setStyleSheet("""
            color: #374151;
            font-size: 13px;
            border: none;
        """)

        layout.addLayout(top_row)
        layout.addWidget(details)

        return card

    def finish(self):
        meter_model = (
            self.xml_data
            .get("MODELO_MEDIDOR", {})
            .get("value", "")
        )

        meter_type = (
            self.xml_data
            .get("TIPO_MEDIDOR", {})
            .get("value", "")
        )

        validation_id = save_validation(
            status=self.validation["final_status"],
            meter_model=meter_model,
            meter_type=meter_type,
            operator_name=self.user["name"],
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        save_divergences(
            validation_id,
            self.validation["divergences"]
        )

        save_validation_items(
            validation_id,
            self.validation["results"]
        )

        self.refresh_callback()
        self.close()