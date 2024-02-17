@echo off

rem Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate

rem Instalar dependencias
pip install -r requirements.txt
