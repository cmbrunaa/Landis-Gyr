import xml.etree.ElementTree as ET


def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = {}

    for var in root.findall("VAR"):
        code = var.get("COD")
        value = var.get("VL")
        technical_value = var.get("IX")

        if code:
            data[code] = {
                "value": value,
                "technical_value": technical_value
            }

    return data