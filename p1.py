from playwright.sync_api import sync_playwright

def buscar_en_google(term):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navegar a Google
        page.goto('https://www.google.com')

        # palabra de busqueda y presionar Enter
        page.fill('input[name="q"]', term)
        page.press('input[name="q"]', 'Enter')

        # Esperar a que aparezcan los resultados
        page.wait_for_selector('div#search')

        # Obtener la cantidad de resultados
        resultados = page.query_selector_all('div.g')
        cantidad_resultados = len(resultados)

        # Cerrar el navegador
        browser.close()

        return cantidad_resultados

if __name__ == "__main__":
    termino_busqueda = "ardillas"
    cantidad_resultados = buscar_en_google(termino_busqueda)
    print(f"Cantidad de resultados para '{termino_busqueda}': {cantidad_resultados}")

# bibliotecas necesarias ejecutando `pip install playwright`. 
# se abre una ventana del navegador (cambiar `headless=True` a `headless=False`)








C
