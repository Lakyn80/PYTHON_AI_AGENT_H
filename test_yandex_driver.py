from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

# Nastavení cesty k Yandex browseru a YandexDriveru
YANDEX_BROWSER_PATH = "C:\\Users\\lukas\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe"
YANDEX_DRIVER_PATH = os.path.abspath("yandexdriver.exe")  # relativní ke kořenovému projektu

# Nastavení options
options = webdriver.ChromeOptions()
options.binary_location = YANDEX_BROWSER_PATH
options.add_argument("--headless")  # volitelně, můžeš odstranit pro ladění

# Inicializace driveru
service = Service(executable_path=YANDEX_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Test – otevřít Yandex
driver.get("https://yandex.ru")
print("🟢 Yandex se úspěšně otevřel.")
driver.quit()
