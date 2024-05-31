import time
import traceback
import argparse
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

def retry(func, *args):
    retries = 10
    while retries > 0:
        try:
            return func(*args)
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            if retries > 0:
                retries -= 1
                print(f"Retries left {retries}, Continuing on {traceback.format_exc()}")
                time.sleep(5)
            else:
                raise e

def demo():
    # Configurar las opciones de ChromeDriver
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-background-networking')
    options.ignore_local_proxy_environment_variables()

    # Ruta específica de Chrome y ChromeDriver
    options.binary_location = '/usr/bin/google-chrome'
    chrome_service = Service('/usr/bin/chromedriver')

    # Inicializar el WebDriver
    driver = webdriver.Chrome(service=chrome_service, options=options)

    # Probar la configuración básica
    try:
        driver.get('https://www.google.com')
        print("Successfully opened Google in headless mode.")
    finally:
        driver.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, nargs='?', help='the config class')
    args = parser.parse_args()

    retry(demo)
