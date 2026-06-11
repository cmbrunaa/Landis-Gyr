PRIMARY_GREEN = "#8CC63F"
DARK_GREEN = "#6DAA2C"
WHITE = "#FFFFFF"

LOGIN_STYLE = f"""
QWidget {{
    background-color: {WHITE};
    font-family: Arial;
}}

QLabel {{
    color: #222222;
    font-size: 14px;
}}

QLineEdit {{
    background-color: #EEF1F5;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
}}

QPushButton {{
    background-color: {PRIMARY_GREEN};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 14px;
    font-size: 15px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {DARK_GREEN};
}}
"""