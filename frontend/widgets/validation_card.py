from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)
from PySide6.QtCore import Qt


class ValidationCard(QFrame):
    def __init__(self, validation, callback):
        super().__init__()

        self.validation = validation
        self.callback = callback

        self.setup_ui()

    def setup_ui(self):
        validation_id = self.validation[0]
        status = self.validation[1]
        model = self.validation[2]
        meter_type = self.validation[3]
        operator = self.validation[4]
        date = self.validation[5]

        color = "#16A34A"
        icon = "✓"

        if status == "REPROVADO":
            color = "#DC2626"
            icon = "✕"
        elif status == "PENDENTE":
            color = "#D97706"
            icon = "!"

        self.setFixedHeight(82)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border-radius: 12px;
                border-left: 5px solid {color};
                border-top: 1px solid #E5E7EB;
                border-right: 1px solid #E5E7EB;
                border-bottom: 1px solid #E5E7EB;
            }}
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(14, 10, 14, 10)
        main_layout.setSpacing(12)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(4)

        title = QLabel(f"Validação #{validation_id}")
        title.setStyleSheet("""
            color: #111827;
            font-size: 15px;
            font-weight: bold;
            border: none;
        """)

        info = QLabel(f"{model} • {meter_type} | Operador: {operator}")
        info.setStyleSheet("""
            color: #6B7280;
            font-size: 12px;
            border: none;
        """)

        date_label = QLabel(str(date))
        date_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 11px;
            border: none;
        """)

        left_layout.addWidget(title)
        left_layout.addWidget(info)
        left_layout.addWidget(date_label)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(8)
        right_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        badge = QLabel(f"{icon} {status}")
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedWidth(110)
        badge.setFixedHeight(26)
        badge.setStyleSheet(f"""
            background-color: #ECFDF3;
            color: {color};
            border-radius: 13px;
            font-size: 11px;
            font-weight: bold;
            border: none;
        """)

        button = QPushButton("Detalhes")
        button.setFixedWidth(90)
        button.setFixedHeight(28)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                background-color: #8CC63F;
                color: white;
                border: none;
                border-radius: 14px;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #79B832;
            }
        """)

        button.clicked.connect(lambda: self.callback(self.validation))

        right_layout.addWidget(badge)
        right_layout.addWidget(button)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout)