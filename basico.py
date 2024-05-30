from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configurar las opciones de ChromeDriver
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

# Ruta específica de Chrome y ChromeDriver
options.binary_location = '/usr/bin/google-chrome'
chrome_service = Service('/usr/local/bin/chromedriver', log_path='/root/PruebasScraping/chromedriver.log')  # Cambia '/path/to/chromedriver.log' a la ruta deseada para el archivo de log

# Inicializar el WebDriver
driver = webdriver.Chrome(service=chrome_service, options=options)

# Abrir una página y verificar el título
driver.get('http://www.google.com')
print(driver.title)

# Cerrar el WebDriver
driver.quit()
