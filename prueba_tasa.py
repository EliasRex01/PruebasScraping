import os
import time
import shutil
import requests
from datetime import datetime
import platform
from colorama import init, Back, Fore
from playwright.sync_api import sync_playwright

# Inicializar colorama
init(autoreset=True)
fecha_actual = datetime.now().strftime('%d/%m/%Y')
tiempo_inicio = time.time()
sistema_operativo = platform.system()

# FUNCION WAIT TRUE
def action(page, selector, value='click'):
    while True:
        try:
            element = page.locator(selector)
            if value == 'click':
                element.click()
            else:
                element.fill(value)
            break
        except Exception as x:
            time.sleep(1)
            continue

# CARGAR EL NUMERO DE JUICIO
juicio = input(Back.WHITE + Fore.RED + "Ingresa Nro de juicio: ")
print(Back.WHITE + Fore.BLUE + "🚀 Iniciar proceso !!")

url = 'https://unionnegocios.com.py/sistema/juicios/datos/' + juicio
try:
    headers = {"Accept": "application/json"}  # Cambiar Content-Type a Accept
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # data['id_juicios']
        cedula = data['ci1']
        monto = data['monto']
        print(Back.WHITE + Fore.BLACK + "--- CI: " + " | DEM: " + data['dem1'] + data['ci1'] + " | MONTO: " + data['monto'])
    else:
        print(f"⚠️ Error.... {response.status_code}")
        sys.exit()
except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit()
print(Back.WHITE + Fore.BLUE + "⌛ procesando....")

# URL del sitio web que deseas procesar
url = 'https://ingresosjudiciales.csj.gov.py/LiquidacionesWeb/loginAbogados.seam'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1200, "height": 1000})
    page.goto(url)

    action(page, '#j_id3\:username', '1591666')  # Usuario
    action(page, '#j_id3\:password', 'estudioAmarillaCloss2')  # Password
    action(page, '#j_id3\:submit', 'click')  # submit
    action(page, '#iconabogadosFormId\:j_id17', 'click')  # Juicios
    action(page, '#iconabogadosFormId\:j_id18', 'click')  # juicio
    action(page, '#juicioFormId\:fechaIdInputDate', fecha_actual)  # Fecha

    # Agregar Demandante
    page.locator('#juicioFormId\:j_id59').click()
    tipo_doc_demandante = page.locator('#juicioFormId\:demandantesListId\:0\:tipoDocumentoContribuyenteId')
    tipo_doc_demandante.select_option(value='1')
    time.sleep(1)
    page.locator('#juicioFormId\:demandantesListId\:0\:numeroDocumentoContribuyenteId').fill('80111738-0')

    # Agregar demandado
    page.locator('xpath=/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[6]/td/table/tbody/tr/td[2]/a').click()
    page.locator('xpath=/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[7]/td/table/tbody/tr/td[2]/input').fill(cedula)

    if data['ci2'] is not None and data['ci2'].isdigit():
        page.locator('xpath=/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[6]/td/table/tbody/tr/td[2]/a').click()
        page.locator('xpath=/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[7]/td/table/tbody/tr[2]/td[2]/input').fill(data['ci2'])

    page.locator('#juicioFormId\:j_id109').click()
    page.locator('xpath=/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/form/span/div/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td[5]/div/input').fill(monto)
    time.sleep(1)
    page.locator('xpath=/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/form/table/tbody/tr/td[1]/input').click()

    # Espera a que aparezca el cuadro de diálogo
    page.locator('xpath=/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td/input').click()
    time.sleep(1)
    page.on("dialog", lambda dialog: dialog.accept())
    print(Back.WHITE + Fore.BLUE + "⚠️ Formulario aceptado")
    
    # Descargar el archivo
    page.locator('xpath=/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td[1]/input').click()
    time.sleep(1)
    browser.close()

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
        # Extrae solo los dígitos del nombre del archivo
        numero_str = ''.join(filter(str.isdigit, archivo))
        if numero_str:
            numero = int(numero_str)
            numero_mas_alto = max(numero_mas_alto, numero)

# Construye el nombre del archivo más alto
nombre_archivo_mas_alto = f"liquidacionJuicio{numero_mas_alto}.pdf"
# Rutas de archivo de origen y carpeta de destino
archivo_a_copiar = os.path.join(carpeta_descargas, nombre_archivo_mas_alto)
path_carpeta_destino = "/Users/cristianamarillacloss/Dropbox/CLIENTES/python"
if sistema_operativo == 'Windows':
    path_carpeta_destino = r'C:\Users\Usuario\Downloads\tasareiniciar'
carpeta_destino = os.path.join(path_carpeta_destino, f"{juicio}-tasa.pdf")
# Copia el archivo a la carpeta de destino y cambia su nombre
shutil.copy(archivo_a_copiar, carpeta_destino)
# Ruta del archivo original en la carpeta de descargas
archivo_original = os.path.join(carpeta_descargas, nombre_archivo_mas_alto)
# Borra el archivo original en la carpeta de descargas
os.remove(archivo_original)

time.sleep(1)
tiempo_fin = time.time()
duracion = round(tiempo_fin - tiempo_inicio)
print(Back.WHITE + Fore.BLUE + "✅ 🎉 FINALIZADO. En " + str(duracion) + " segundos !!!")
