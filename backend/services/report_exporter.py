import csv
from pathlib import Path
from datetime import datetime

from database.validation_repository import get_validations


def export_validations_to_csv(validations=None):
    if validations is None:
        validations = get_validations()

    project_root = Path(__file__).resolve().parents[2]

    exports_dir = project_root / "exports"
    exports_dir.mkdir(exist_ok=True)

    file_name = f"validacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = exports_dir / file_name

    with open(
        file_path,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file, delimiter=";")

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