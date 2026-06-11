import csv
from pathlib import Path

from database.validation_repository import get_validations


def export_validations_to_csv():
    validations = get_validations()

    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)

    file_path = exports_dir / "validacoes.csv"

    with open(
        file_path,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Status",
            "Modelo",
            "Tipo",
            "Operador",
            "Data"
        ])

        for validation in validations:
            writer.writerow(validation)

    return str(file_path)