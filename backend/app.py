import os
from datetime import datetime

from services.xml_reader import read_xml
from services.validator import validate_parameters
from services.auth_service import login
from database.database import create_tables
from database.user_repository import create_user, find_user_by_username
from database.validation_repository import (
    save_validation,
    save_divergences,
    get_validations,
    get_divergences,
    get_dashboard_summary,
    get_validations_by_operator
)
from reports.csv_exporter import export_validations_to_csv
from utils.password import hash_password

def create_default_admin():
    admin = find_user_by_username("admin")

    if admin is None:
        create_user(
            name="Administrador",
            username="admin",
            password=hash_password("123"),
            role="GESTOR",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )


def login_menu():
    print("\nLOGIN\n")

    username = input("Usuário: ").strip().lower()
    password = input("Senha: ")

    user = login(username, password)

    if user is None:
        print("\nUsuário ou senha inválidos.")
        return None

    print(f"\nBem-vindo, {user['username']} | Perfil: {user['role']}\n")
    return user


def validate_xml(user):

    file_path = input(
        "\nDigite o caminho do XML: "
    ).strip()

    if not os.path.exists(file_path):
        print("\nArquivo não encontrado.")
        return

    xml_data = read_xml(file_path)
    validation = validate_parameters(xml_data)

    meter_model = xml_data.get("MODELO_MEDIDOR", {}).get("value", "")
    meter_type = xml_data.get("TIPO_MEDIDOR", {}).get("value", "")

    validation_id = save_validation(
        status=validation["final_status"],
        meter_model=meter_model,
        meter_type=meter_type,
        operator_name=user["name"],
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    save_divergences(validation_id, validation["divergences"])

    print("\nRESULTADO DA VALIDAÇÃO:\n")
    print(f"Validação salva com ID: {validation_id}")
    print(f"Status final: {validation['final_status']}\n")

    for item in validation["results"]:
        print(f"{item['status']} | {item['parameter']}")
        print(f"  Esperado: {item['expected']}")
        print(f"  Encontrado: {item['found']}")
        print(f"  Mensagem: {item['message']}\n")

    divergences = get_divergences(validation_id)

    print("\nDIVERGÊNCIAS:\n")

    if not divergences:
        print("Nenhuma divergência encontrada.")
    else:
        for item in divergences:
            print(f"Parâmetro: {item[0]}")
            print(f"Esperado: {item[1]}")
            print(f"Encontrado: {item[2]}")
            print(f"Mensagem: {item[3]}\n")


def show_dashboard():
    summary = get_dashboard_summary()

    print("\nDASHBOARD:\n")

    print(f"Total de validações: {summary['total']}")
    print(f"Confirmadas: {summary['confirmed']}")
    print(f"Reprovadas: {summary['reproved']}")
    print(f"Pendentes: {summary['pending']}")

    print("\nVALIDAÇÕES POR OPERADOR:\n")

    operators = get_validations_by_operator()

    if not operators:
        print("Nenhuma validação encontrada.")
        return

    for operator in operators:
        print(
            f"{operator[0]}: {operator[1]} validações"
        )

def show_history():
    validations = get_validations()

    print("\nHISTÓRICO:\n")

    if not validations:
        print("Nenhuma validação encontrada.")
        return

    for item in validations:
        validation_id = item[0]
        status = item[1]
        meter_model = item[2]
        meter_type = item[3]
        operator_name = item[4]
        created_at = item[5]

        print("=" * 40)
        print(f"ID: {validation_id}")
        print(f"Status: {status}")
        print(f"Modelo: {meter_model}")
        print(f"Tipo: {meter_type}")
        print(f"Operador: {operator_name}")
        print(f"Data: {created_at}")
        print("=" * 40)


def export_csv():
    csv_path = export_validations_to_csv()
    print(f"\nCSV gerado em: {csv_path}")


def create_user_menu(current_user):
    if current_user["role"] != "GESTOR":
        print("\nApenas usuários gestores podem cadastrar novos usuários.")
        return

    print("\nCADASTRAR USUÁRIO\n")

    name = input("Nome: ").strip()
    username = input("Usuário: ").strip().lower()
    password = input("Senha: ").strip()
    role = input("Perfil (OPERADOR/GESTOR): ").strip().upper()

    if not name or not username or not password:
        print("\nTodos os campos são obrigatórios.")
        return

    if role not in ["OPERADOR", "GESTOR"]:
        print("\nPerfil inválido. Use OPERADOR ou GESTOR.")
        return

    existing_user = find_user_by_username(username)

    if existing_user is not None:
        print("\nJá existe um usuário com esse login.")
        return

    create_user(
        name=name,
        username=username,
        password=hash_password(password),
        role=role,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    print("\nUsuário cadastrado com sucesso.")


def main_menu(user):
    while True:
        print("\n==============================")
        print(" FIRST OFF - LANDIS+GYR")
        print("==============================")
        print("1 - Validar XML")

        if user["role"] == "GESTOR":
            print("2 - Ver dashboard")

        print("3 - Ver histórico")

        if user["role"] == "GESTOR":
            print("4 - Exportar CSV")
            print("5 - Cadastrar usuário")

        print("0 - Sair")

        option = input("\nEscolha uma opção: ")

        if option == "1":
            validate_xml(user)
        elif option == "2" and user["role"] == "GESTOR":
            show_dashboard()
        elif option == "3":
            show_history()
        elif option == "4" and user["role"] == "GESTOR":
            export_csv()
        elif option == "5" and user["role"] == "GESTOR":
            create_user_menu(user)
        elif option == "0":
            print("\nSaindo do sistema...")
            break
        else:
            print("\nOpção inválida ou sem permissão.")

def main():
    create_tables()
    create_default_admin()

    user = login_menu()

    if user is None:
        return

    main_menu(user)


if __name__ == "__main__":
    main()