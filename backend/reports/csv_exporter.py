import csv
from pathlib import Path

from database.validation_repository import get_validations


def export_validations_to_csv():

    validations = get_validations()

    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)

    file_path = exports_dir / "historico_validacoes.csv"

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
            "Modelo do Medidor",
            "Tipo do Medidor",
            "Operador",
            "Data"
        ])

        for validation in validations:
            writer.writerow(validation)

    print(f"CSV gerado em: {file_path.resolve()}")

    return str(file_path.resolve())