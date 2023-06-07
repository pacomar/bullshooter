Crear entorno
`python3 -m venv myvenv`

Activar entorno
`source myvenv/bin/activate`

Actualziar pip
`python -m pip install --upgrade pip`

Para actualizar el archivo de dependencias:

`python -m pip freeze > requirements.txt`

Para instalar las dependencias:

`python -m pip install -r requirements.txt`

Ejecutar migraciones sobre la bbdd
`python manage.py migrate`

Ejecutar servidor
`python manage.py runserver`