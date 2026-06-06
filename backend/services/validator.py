from config.rules import EXPECTED_RULES


def validate_parameters(xml_data):
    results = []
    divergences = []

    for code, expected_value in EXPECTED_RULES.items():
        found_info = xml_data.get(code)

        if found_info is None:
            result = {
                "parameter": code,
                "expected": expected_value,
                "found": "Não encontrado",
                "status": "PENDENTE",
                "message": "Parâmetro não encontrado no XML."
            }

            results.append(result)
            divergences.append(result)
            continue

        found_value = found_info["value"]

        if found_value == expected_value:
            result = {
                "parameter": code,
                "expected": expected_value,
                "found": found_value,
                "status": "CONFIRMADO",
                "message": "Parâmetro correto."
            }
        else:
            result = {
                "parameter": code,
                "expected": expected_value,
                "found": found_value,
                "status": "REPROVADO",
                "message": "Valor diferente do esperado."
            }

            divergences.append(result)

        results.append(result)

    final_status = "CONFIRMADO" if len(divergences) == 0 else "REPROVADO"

    return {
        "final_status": final_status,
        "results": results,
        "divergences": divergences
    }