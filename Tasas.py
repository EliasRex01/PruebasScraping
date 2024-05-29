import os
import platform
import time
import requests
import shutil
from abc import ABC, ABCMeta, abstractmethod
from datetime import datetime
from colorama import init, Back, Fore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Inicializar colorama
init(autoreset=True)

# Clase base abstracta
class ProcesoJudicial(ABC):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def ejecutar_proceso(self, juicio, data):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

# Clase concreta que implementa el proceso judicial con Selenium
class ProcesoJudicialSelenium(ProcesoJudicial):
    def __init__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-software-rasterizer')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1200, 1000)
        self.wait = WebDriverWait(self.driver, 10)

    def ejecutar_proceso(self, juicio, data):
        fecha_actual = datetime.now().strftime('%d/%m/%Y')
        url = 'https://ingresosjudiciales.csj.gov.py/LiquidacionesWeb/loginAbogados.seam'
        self.driver.get(url)

        # Iniciar sesión
        self.action('j_id3:username', '1591666')
        self.action('j_id3:password', 'estudioAmarillaCloss2')
        self.action('j_id3:submit', 'click')

        # Navegar por el sitio
        self.action('iconabogadosFormId:j_id17', 'click')
        self.action('iconabogadosFormId:j_id18', 'click')
        self.action('juicioFormId:fechaIdInputDate', fecha_actual)

        # Agregar Demandante
        self.wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:j_id59'))).click()
        tipo_doc_demandante = Select(self.wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:demandantesListId:0:tipoDocumentoContribuyenteId'))))
        tipo_doc_demandante.select_by_value('1')
        time.sleep(1)
        nro_doc_demandante = self.driver.find_element(By.ID, 'juicioFormId:demandantesListId:0:numeroDocumentoContribuyenteId')
        nro_doc_demandante.send_keys('80111738-0')

        # Agregar demandado
        self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[6]/td/table/tbody/tr/td[2]/a'))).click()
        nro_doc_demandado = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[7]/td/table/tbody/tr/td[2]/input')))
        nro_doc_demandado.send_keys(data['ci1'])

        if data['ci2'] is not None and data['ci2'].isdigit():
            self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[6]/td/table/tbody/tr/td[2]/a'))).click()
            nro_doc_demandado2 = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/span/table[1]/tbody/tr[7]/td/table/tbody/tr[2]/td[2]/input')))
            nro_doc_demandado2.send_keys(data['ci2'])

        # Agregar concepto y monto
        self.wait.until(EC.element_to_be_clickable((By.ID, 'juicioFormId:j_id109'))).click()
        self.wait.until(EC.element_to_be_clickable((By.NAME, 'modalPanelFormId:conceptosListId:5:j_id196'))).click()
        agregarMonto = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/form/span/div/div/div[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td[5]/div/input')))
        agregarMonto.send_keys(data['monto'])
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/form/table/tbody/tr/td[1]/input'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td/input'))).click()
        time.sleep(1)
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
        alert.accept()
        print(Back.WHITE + Fore.BLUE + "⚠️ Formulario aceptado")

        # Descargar la tasa judicial
        time.sleep(1)
        self.driver.find_element(By.XPATH, '/html/body/table/tbody/tr[5]/td/div/div/table/tbody/tr/td[2]/table/tbody/tr[6]/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td/form/table/tbody/tr/td[1]/input').click()

        # Mover archivo descargado
        carpeta_descargas = "/Users/cristianamarillacloss/Downloads"
        if platform.system() == 'Windows':
            carpeta_descargas = r'C:\Users\Usuario\Downloads'

        archivos_en_descargas = os.listdir(carpeta_descargas)
        numero_mas_alto = max([int(''.join(filter(str.isdigit, archivo))) for archivo in archivos_en_descargas if archivo.startswith("liquidacionJuicio") and archivo.endswith(".pdf")], default=0)
        nombre_archivo_mas_alto = f"liquidacionJuicio{numero_mas_alto}.pdf"

        archivo_a_copiar = os.path.join(carpeta_descargas, nombre_archivo_mas_alto)
        path_carpeta_destino = "/Users/cristianamarillacloss/Dropbox/CLIENTES/python"
        if platform.system() == 'Windows':
            path_carpeta_destino = r'C:\Users\Usuario\Downloads\tasareiniciar'
        carpeta_destino = os.path.join(path_carpeta_destino, f"{juicio}-tasa.pdf")
        shutil.copy(archivo_a_copiar, carpeta_destino)
        os.remove(archivo_a_copiar)
        time.sleep(1)

    def action(self, path='', value='click'):
        while True:
            try:
                element = self.driver.find_element(By.XPATH, path) if '/' in path else self.driver.find_element(By.ID, path)
                if value == 'click':
                    element.click()
                else:
                    element.send_keys(value)
            except Exception:
                time.sleep(1)
                continue
            break

# Clase para manejar la consulta
class Consulta:
    def __init__(self):
        self.proceso_judicial = ProcesoJudicialSelenium()

    def ejecutar(self, juicio):
        url = f'https://unionnegocios.com.py/sistema/juicios/datos/{juicio}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(Back.WHITE + Fore.BLACK + f"--- CI: | DEM: {data['dem1']} {data['ci1']} | MONTO: {data['monto']}")
                self.proceso_judicial.ejecutar_proceso(juicio, data)
            else:
                print(f"⚠️ Error.... {response.status_code}")
        except requests.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")

# Función principal
def main():
    consulta = Consulta()
    while True:
        juicio = input("Ingrese el número de juicio (o 'salir' para terminar): ")
        if juicio.lower() == 'salir':
            break
        if juicio.isdigit():
            consulta.ejecutar(juicio)
        else:
            print("Por favor, ingrese un número de juicio válido.")

if __name__ == "__main__":
    main()