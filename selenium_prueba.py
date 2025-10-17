
# AUTOMATIZACIÓN DE TAREAS WEB CON SELENIUM
# --------------------------------------------------
# Este script sirve para automatizar procesos en un sitio web:
# 1️⃣ Abrir un navegador y acceder a una página web automáticamente.
# 2️⃣ Buscar y extraer información de los elementos de la página (ej. títulos, precios).
# 3️⃣ Interactuar con la página de forma automática (clics, navegación entre páginas, movimientos del mouse).
# 4️⃣ Guardar datos obtenidos en archivos para su análisis posterior (ej. CSV, capturas de pantalla).

from selenium import webdriver  # importa la API principal de Selenium para controlar navegadores
from selenium.webdriver.chrome.service import Service  # clase para gestionar el servicio/ejecutable del ChromeDriver
from selenium.webdriver.common.by import By  # constantes para localizar elementos (By.ID, By.XPATH, etc.)
from selenium.webdriver.common.keys import Keys  # constantes para teclas especiales (Keys.ENTER, Keys.TAB, ...)
from selenium.webdriver.support.ui import WebDriverWait  # utilidad para esperas explícitas (esperar condiciones)
from selenium.webdriver.support import expected_conditions as EC  # condiciones predefinidas usadas con WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains  # para acciones complejas (arrastrar, mover, secuencias de teclas)
from webdriver_manager.chrome import ChromeDriverManager  # gestiona la descarga/actualización automática del ChromeDriver
import time, csv, os  # módulos estándar: time (pausas/sleep), csv (leer/escribir CSV), os (operaciones del sistema/patrones de ruta)

# --------------------------------------------
# CONFIGURACIÓN DEL NAVEGADOR
# --------------------------------------------
options = webdriver.ChromeOptions() # Configuraciones para el navegador Chrome
options.add_argument("--start-maximized")  # Abre la ventana en pantalla completa
options.add_argument("--disable-blink-features=AutomationControlled")  # puede ayudar a reducir la detección por Selenium, pero no es efectivo contra sistemas avanzados y puede romper funcionalidades de algunos sitios.
options.add_experimental_option("detach", True)  # Mantiene abierta la ventana

# Usa el ChromeDriver desde el caché de webdriver_manager (descarga solo si no está presente)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10) #webdriver espera hasta 10 segundos para ciertas condiciones
actions = ActionChains(driver)  # Permite hacer movimientos del mouse y combinaciones de teclas

# --------------------------------------------
# ABRIR UNA PÁGINA
# --------------------------------------------
driver.get("https://books.toscrape.com/")
print("Página abierta:", driver.title)

# --------------------------------------------
# ENCONTRAR ELEMENTOS
# --------------------------------------------
# find_elements → busca varios elementos (lista)
books = driver.find_elements(By.CLASS_NAME, "product_pod") #busca todos los libros en la página por su clase
print(f"Se encontraron {len(books)} libros en la página 1.\n") # Muestra la cantidad de libros encontrados

# --------------------------------------------
# EXTRAER INFORMACIÓN DE LOS ELEMENTOS
# --------------------------------------------
for i, book in enumerate(books[:5], 1):  # Ciclo por solo los primeros 5 
    title = book.find_element(By.TAG_NAME, "h3").text # Busca el título del libro
    price = book.find_element(By.CLASS_NAME, "price_color").text # Busca el precio del libro
    print(f"{i}. {title} - {price}") # Muestra título y precio

# --------------------------------------------
# HACER CLIC EN UN ELEMENTO
# --------------------------------------------
# Hacemos clic en el primer libro
books[0].find_element(By.TAG_NAME, "h3").click()

# Esperar que cargue la nueva página
wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))) # Esperar que el título del libro esté presente
print("\nEntramos al detalle del libro:", driver.find_element(By.TAG_NAME, "h1").text) # extrae y muestra el título del libro

# --------------------------------------------
# NAVEGAR HACIA ATRÁS
# --------------------------------------------
driver.back()
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod"))) # Esperar que cargue la página de libros

# --------------------------------------------
# USAR ActionChains
# --------------------------------------------
libro = driver.find_elements(By.CLASS_NAME, "product_pod")[1] # Busca el segundo libro
actions.move_to_element(libro).double_click().perform() # Se mueve y hacEe doble clic en el libro

# --------------------------------------------
# CAMBIAR ENTRE PÁGINAS
# --------------------------------------------
driver.back()
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod"))) # Esperar que cargue la página de libros

next_btn = driver.find_element(By.CSS_SELECTOR, "li.next > a") # Botón "next"
next_btn.click()
print("\nPasamos a la página 2.")
print("URL actual:", driver.current_url) # URL actual

# --------------------------------------------
# GUARDAR DATOS EN CSV
# --------------------------------------------
books = driver.find_elements(By.CLASS_NAME, "product_pod") # Libros en la página 2


csv_filename = "libros.csv" # Nombre del archivo CSV
with open(csv_filename, "w", newline="", encoding="utf-8") as file: # Abrir archivo para escritura
    writer = csv.writer(file) # Crear objeto escritor CSV
    writer.writerow(["Titulo", "Precio"]) # Escribir encabezados
    for book in books: # Iterar sobre los libros
        title = book.find_element(By.TAG_NAME, "h3").text # Toma el título del libro
        price = book.find_element(By.CLASS_NAME, "price_color").text # Toma el precio del libro
        writer.writerow([title, price]) # Escribir fila con título y precio

# Mostramos la ruta absoluta donde se guardó el archivo
csv_path = os.path.abspath(csv_filename)
print(f"✅ Datos guardados en '{csv_filename}'") #Nombre del archivo
print(f"📂 Archivo CSV guardado en: {csv_path}") #Ruta 

# --------------------------------------------
#   ESPERAR ANTES DE CERRAR
# --------------------------------------------
input("\nPresiona ENTER para cerrar...")
driver.quit()
