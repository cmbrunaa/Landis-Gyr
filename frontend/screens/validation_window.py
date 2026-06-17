from frontend.screens.validation_review_window import ValidationReviewWindow

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

        self.file_label = QLabel(
            "Nenhum arquivo selecionado"
        )

        select_button = QPushButton(
            "Selecionar XML"
        )

        select_button.clicked.connect(
            self.select_xml
        )

        layout.addWidget(title)
        layout.addWidget(self.file_label)
        layout.addWidget(select_button)
        layout.addStretch()

    def select_xml(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar XML",
            "",
            "Arquivos XML (*.xml *.txt)"
        )

        if not file_path:
            return

        self.file_label.setText(file_path)

        try:
            xml_data = read_xml(file_path)

            validation = validate_parameters(
                xml_data
            )

            self.review_window = ValidationReviewWindow(
                user=self.user,
                validation=validation,
                xml_data=xml_data,
                refresh_callback=self.refresh_callback
            )

            self.review_window.show()
            self.hide()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Erro",
                str(error)
            )