import csv
import os

from database.validation_repository import get_validations


def export_validations_to_csv():
    validations = get_validations()

    os.makedirs("../exports", exist_ok=True)

    file_path = "../exports/historico_validacoes.csv"

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Status",
            "Modelo do Medidor",
            "Tipo do Medidor",
            "Data"
        ])

        for validation in validations:
            writer.writerow(validation)

    return file_path