from config.rules import EXPECTED_RULES


def validate_parameters(xml_data):

    results = []

    confirmed = 0
    pending = 0
    divergent = 0

    divergences = []

    for code, expected_value in EXPECTED_RULES.items():

        found = xml_data.get(code)

        if not found:

            result = {
                "parameter": code,
                "expected": expected_value,
                "found": "",
                "status": "PENDENTE",
                "message": "Parâmetro não encontrado"
            }

            pending += 1
            divergences.append(result)

        else:

            found_value = found["value"]

            if found_value == expected_value:

                result = {
                    "parameter": code,
                    "expected": expected_value,
                    "found": found_value,
                    "status": "CONFIRMADO",
                    "message": "Valor validado"
                }

                confirmed += 1

            else:

                result = {
                    "parameter": code,
                    "expected": expected_value,
                    "found": found_value,
                    "status": "DIVERGENTE",
                    "message": "Valor diferente"
                }

                divergent += 1
                divergences.append(result)

        results.append(result)

    total = len(results)

    conformity = round(
        (confirmed / total) * 100,
        0
    ) if total else 0

    return {
        "results": results,
        "divergences": divergences,
        "confirmed": confirmed,
        "pending": pending,
        "divergent": divergent,
        "total": total,
        "conformity": conformity
    }