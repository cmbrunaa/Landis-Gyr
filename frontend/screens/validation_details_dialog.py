from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QWidget
)

from database.validation_repository import get_divergences


class ValidationDetailsDialog(QDialog):
    def __init__(self, validation):
        super().__init__()

        self.validation = validation

        self.setWindowTitle("Detalhes da Validação")
        self.setFixedSize(520, 420)
        self.setStyleSheet("""
            QDialog {
                background-color: #F4F6F8;
            }

            QLabel {
                color: #333333;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        validation_id = validation[0]
        status = validation[1]
        meter_model = validation[2]
        meter_type = validation[3]
        operator_name = validation[4]
        created_at = validation[5]

        title = QLabel(f"Validação #{validation_id}")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #222222;
        """)

        status_label = QLabel(f"Status: {status}")
        status_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #8CC63F;
        """)

        info = QLabel(
            f"Modelo: {meter_model}\n"
            f"Tipo: {meter_type}\n"
            f"Operador: {operator_name}\n"
            f"Data: {created_at}"
        )

        divergences_title = QLabel("Divergências")
        divergences_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            margin-top: 15px;
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        content = QWidget()
        content_layout = QVBoxLayout(content)

        divergences = get_divergences(validation_id)

        if not divergences:
            ok_card = QFrame()
            ok_card.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    border: 1px solid #DDE3EA;
                }
            """)

            ok_layout = QVBoxLayout(ok_card)

            ok_label = QLabel("✅ Nenhuma divergência encontrada.")
            ok_label.setStyleSheet("""
                color: #16A34A;
                font-size: 15px;
                font-weight: bold;
            """)

            ok_layout.addWidget(ok_label)
            content_layout.addWidget(ok_card)

        else:
            for item in divergences:
                parameter = item[0]
                expected = item[1]
                found = item[2]
                message = item[3]

                card = QFrame()
                card.setStyleSheet("""
                    QFrame {
                        background-color: #FFFFFF;
                        border-radius: 10px;
                        border: 1px solid #DDE3EA;
                    }
                """)

                card_layout = QVBoxLayout(card)

                parameter_label = QLabel(f"❌ {parameter}")
                parameter_label.setStyleSheet("""
                    color: #DC2626;
                    font-size: 15px;
                    font-weight: bold;
                """)

                details = QLabel(
                    f"Esperado: {expected}\n"
                    f"Encontrado: {found}\n"
                    f"Mensagem: {message}"
                )

                card_layout.addWidget(parameter_label)
                card_layout.addWidget(details)

                content_layout.addWidget(card)

        content_layout.addStretch()
        scroll.setWidget(content)

        layout.addWidget(title)
        layout.addWidget(status_label)
        layout.addWidget(info)
        layout.addWidget(divergences_title)
        layout.addWidget(scroll)