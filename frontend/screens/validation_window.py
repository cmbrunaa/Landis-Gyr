from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from services.xml_reader import read_xml
from services.validator import validate_parameters

from database.validation_repository import save_validation, save_divergences


class ValidationWindow(QWidget):
    def __init__(self, user, refresh_callback):
        super().__init__()

        self.user = user
        self.refresh_callback = refresh_callback

        layout = QVBoxLayout(self)

        title = QLabel("Validação de XML")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        self.file_label = QLabel("Nenhum arquivo selecionado")

        select_button = QPushButton("Selecionar XML")
        select_button.clicked.connect(self.select_xml)

        layout.addWidget(title)
        layout.addWidget(self.file_label)
        layout.addWidget(select_button)
        layout.addStretch()

    def select_xml(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar XML", "", "Arquivos XML (*.xml *.txt)"
        )

        if not file_path:
            return

        self.file_label.setText(file_path)

        try:
            xml_data = read_xml(file_path)

            validation = validate_parameters(xml_data)

            meter_model = xml_data.get("MODELO_MEDIDOR", {}).get("value", "")

            meter_type = xml_data.get("TIPO_MEDIDOR", {}).get("value", "")

            validation_id = save_validation(
                status=validation["final_status"],
                meter_model=meter_model,
                meter_type=meter_type,
                operator_name=self.user["name"],
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            save_divergences(validation_id, validation["divergences"])

            QMessageBox.information(
                self,
                "Validação concluída",
                f"Status: {validation['final_status']}\n\nID: {validation_id}",
            )

            self.refresh_callback()
            self.close()

        except Exception as error:
            QMessageBox.critical(self, "Erro", str(error))
