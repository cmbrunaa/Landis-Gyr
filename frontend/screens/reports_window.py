from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox,
    QComboBox,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Qt

from database.validation_repository import get_validations
from services.report_exporter import export_validations_to_csv


class ReportsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent_window = parent
        self.validations = get_validations()

        self.setStyleSheet("background-color: #F4F6F8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(18)

        title = QLabel("Relatórios")
        title.setStyleSheet("""
            color: #111827;
            font-size: 30px;
            font-weight: bold;
            border: none;
        """)

        subtitle = QLabel("Filtre as validações realizadas e exporte os resultados em CSV.")
        subtitle.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            border: none;
        """)

        filters_panel = self.create_filters_panel()
        results_panel = self.create_results_panel()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(filters_panel)
        layout.addWidget(results_panel)
        layout.addStretch()

    def create_filters_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E1E5EA;
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Filtros do Relatório")
        title.setStyleSheet("""
            color: #111827;
            font-size: 20px;
            font-weight: bold;
            border: none;
        """)

        filters_row = QHBoxLayout()
        filters_row.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar por modelo ou operador")

        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "Todos",
            "CONFIRMADO",
            "DIVERGENTE",
            "PENDENTE"
        ])

        export_button = QPushButton("Exportar CSV")
        export_button.clicked.connect(self.export_csv)

        self.search_input.textChanged.connect(self.apply_filters)
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        for field in [self.search_input, self.status_filter]:
            field.setFixedHeight(42)
            field.setStyleSheet("""
                background-color: #F4F6F8;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            """)

        export_button.setFixedHeight(42)
        export_button.setCursor(Qt.PointingHandCursor)
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #8CC63F;
                color: #FFFFFF;
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

        filters_row.addWidget(self.search_input, 2)
        filters_row.addWidget(self.status_filter, 1)
        filters_row.addWidget(export_button)

        layout.addWidget(title)
        layout.addLayout(filters_row)

        return panel

    def create_results_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #E1E5EA;
            }
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(14)

        self.result_label = QLabel(f"Resultados encontrados: {len(self.validations)}")
        self.result_label.setStyleSheet("""
            color: #111827;
            font-size: 18px;
            font-weight: bold;
            border: none;
        """)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Status",
            "Modelo",
            "Tipo",
            "Operador",
            "Data"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setStyleSheet("""
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

        self.load_table(self.validations)

        layout.addWidget(self.result_label)
        layout.addWidget(self.table)

        return panel

    def load_table(self, validations):
        self.table.setRowCount(len(validations))

        for row, validation in enumerate(validations):
            validation_id = validation[0]
            status = validation[1]
            meter_model = validation[2]
            meter_type = validation[3]
            operator_name = validation[4]
            created_at = validation[5]

            values = [
                validation_id,
                status,
                meter_model,
                meter_type,
                operator_name,
                created_at
            ]

            for col, value in enumerate(values):
                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(str(value))
                )

    def apply_filters(self):
        search = self.search_input.text().strip().lower()
        status = self.status_filter.currentText()

        filtered = []

        for validation in get_validations():
            validation_status = validation[1]
            meter_model = str(validation[2]).lower()
            operator_name = str(validation[4]).lower()

            matches_search = (
                search in meter_model
                or search in operator_name
                or search == ""
            )

            matches_status = (
                status == "Todos"
                or validation_status == status
            )

            if matches_search and matches_status:
                filtered.append(validation)

        self.validations = filtered
        self.result_label.setText(f"Resultados encontrados: {len(filtered)}")
        self.load_table(filtered)

    def export_csv(self):
        file_path = export_validations_to_csv(self.validations)

        QMessageBox.information(
            self,
            "Exportação concluída",
            f"Arquivo gerado em:\n\n{file_path}"
        )