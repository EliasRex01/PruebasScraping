import requests
import json
from datetime import datetime
import platform
import os
import shutil
import time

# Inicializar parámetros
fecha_actual = datetime.now().strftime('%d/%m/%Y')
tiempo_inicio = time.time()
sistema_operativo = platform.system()

# Obtener número de juicio
juicio = input("Ingresa Nro de juicio: ")
print("🚀 Iniciar proceso !!")

# URL para obtener datos del juicio
url_datos_juicio = f'https://unionnegocios.com.py/sistema/juicios/datos/{juicio}'

# Obtener datos del juicio en formato JSON
try:
    headers = {"Accept": "application/json"}
    response = requests.get(url_datos_juicio, headers=headers)
    response.raise_for_status()
    data = response.json()
    cedula = data['ci1']
    monto = data['monto']
    print(f"--- CI: {cedula} | DEM: {data['dem1']} {cedula} | MONTO: {monto}")
except requests.RequestException as e:
    print(f"Error al obtener datos del juicio: {e}")
    exit()

# URL para el inicio de sesión (asumiendo que existe una API)
url_login = 'https://ingresosjudiciales.csj.gov.py/api/login'
login_payload = {
    'username': '1591666',
    'password': 'estudioAmarillaCloss2'
}

# Realizar el inicio de sesión
try:
    response = requests.post(url_login, json=login_payload, headers=headers)
    response.raise_for_status()
    auth_token = response.json().get('token')
except requests.RequestException as e:
    print(f"Error al iniciar sesión: {e}")
    exit()

# Headers con el token de autenticación
auth_headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {auth_token}"
}

# URL para enviar datos del juicio
url_procesar_juicio = 'https://ingresosjudiciales.csj.gov.py/api/juicio'

# Payload para procesar el juicio (ejemplo)
juicio_payload = {
    'fecha': fecha_actual,
    'demandantes': [{'tipo_documento': '1', 'numero_documento': '80111738-0'}],
    'demandados': [{'numero_documento': cedula}],
    'monto': monto
}

# Enviar datos del juicio
try:
    response = requests.post(url_procesar_juicio, json=juicio_payload, headers=auth_headers)
    response.raise_for_status()
    print("⚠️ Formulario aceptado")
except requests.RequestException as e:
    print(f"Error al procesar el juicio: {e}")
    exit()

# Ruta de la carpeta de descargas
carpeta_descargas = "/Users/cristianamarillacloss/Downloads"
if sistema_operativo == 'Windows':
    carpeta_descargas = r'C:\Users\Usuario\Downloads'

# Obtener una lista de archivos en la carpeta de descargas
archivos_en_descargas = os.listdir(carpeta_descargas)

# Inicializa la variable para el número más alto
numero_mas_alto = 0

# Busca el número más alto en los nombres de los archivos
for archivo in archivos_en_descargas:
    if archivo.startswith("liquidacionJuicio") and archivo.endswith(".pdf"):
        numero_str = ''.join(filter(str.isdigit, archivo))
        if numero_str:
            numero = int(numero_str)
            numero_mas_alto = max(numero_mas_alto, numero)

# Construye el nombre del archivo más alto
nombre_archivo_mas_alto = f"liquidacionJuicio{numero_mas_alto}.pdf"
archivo_a_copiar = os.path.join(carpeta_descargas, nombre_archivo_mas_alto)
path_carpeta_destino = "/Users/cristianamarillacloss/Dropbox/CLIENTES/python"
if sistema_operativo == 'Windows':
    path_carpeta_destino = r'C:\Users\Usuario\Downloads\tasareiniciar'
carpeta_destino = os.path.join(path_carpeta_destino, f"{juicio}-tasa.pdf")

# Copia el archivo a la carpeta de destino y cambia su nombre
shutil.copy(archivo_a_copiar, carpeta_destino)
os.remove(archivo_a_copiar)

tiempo_fin = time.time()
duracion = round(tiempo_fin - tiempo_inicio)
print(f"✅  🎉  FINALIZADO. En {duracion} segundos !!!")
