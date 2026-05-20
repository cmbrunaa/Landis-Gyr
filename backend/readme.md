1- Verificar se o python está instalado com "python -m pip install lxml"


Após, instalar: 

python -m pip install fastapi
python -m pip install uvicorn
python -m pip install sqlalchemy
python -m pip install lxml

--------- PULE PARA A LINHA 32

Para evitar problemas em outros computadores rode:

python -m venv venv

E em seguida ative: 

.\venv\Scripts\Activate

Caso algum erro ocorra, modifique as politicas da máquina com o seguinte comando no powershell:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
"Deseja alterar a política?
[S] Sim  [A] Sim para todos"

Teste novamente: 

.\venv\Scripts\Activate

Após, instalar as bibliotecas: 

python -m pip install fastapi uvicorn sqlalchemy lxml

--------- DEMAIS INTEGRANTES -----------

pip install -r requirements.txt

