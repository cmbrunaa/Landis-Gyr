from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit
)

from database.validation_repository import (
    save_validation,
    save_divergences
)


class ValidationReviewWindow(QWidget):

    def __init__(
        self,
        user,
        validation,
        xml_data,
        refresh_callback
    ):

        super().__init__()

        self.user = user
        self.validation = validation
        self.xml_data = xml_data
        self.refresh_callback = refresh_callback

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Revisão da Validação")
        )

        details = QTextEdit()

        details.setReadOnly(True)

        text = ""

        for item in validation["results"]:

            text += (
                f"{item['parameter']}\n"
                f"{item['status']}\n\n"
            )

        text += "\n"

        text += (
            f"Confirmados: {validation['confirmed']}\n"
            f"Pendentes: {validation['pending']}\n"
            f"Divergentes: {validation['divergent']}\n"
            f"Conformidade: {validation['conformity']}%"
        )

        details.setText(text)

        layout.addWidget(details)

        save_btn = QPushButton(
            "Finalizar Validação"
        )

        save_btn.clicked.connect(
            self.finish
        )

        layout.addWidget(save_btn)

    def finish(self):

        meter_model = (
            self.xml_data
            .get(
                "MODELO_MEDIDOR",
                {}
            )
            .get(
                "value",
                ""
            )
        )

        meter_type = (
            self.xml_data
            .get(
                "TIPO_MEDIDOR",
                {}
            )
            .get(
                "value",
                ""
            )
        )

        validation_id = save_validation(

            status="FINALIZADO",

            meter_model=meter_model,

            meter_type=meter_type,

            operator_name=self.user["name"],

            created_at=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )

        save_divergences(
            validation_id,
            self.validation["divergences"]
        )

        self.refresh_callback()

        self.close()