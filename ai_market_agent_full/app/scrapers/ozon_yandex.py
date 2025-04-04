from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from app.models import ProductEntry
from app.db import db
import os

def scrape_ozon_yandex():
    url = "https://www.ozon.ru/search/?text=суставы"

    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\Users\\lukas\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=os.path.abspath("yandexdriver.exe"))
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(6)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    cards = soup.select("div[data-widget='searchResultsV2'] a")

    for card in cards[:20]:
        try:
            title = card.get_text(strip=True)
            href = card.get("href")
            product_url = f"https://ozon.ru{href}"

            product = ProductEntry(
                platform="ozon",
                title=title,
                product_url=product_url
            )
            db.session.add(product)

        except Exception as e:
            print("Ozon Yandex error:", e)

    db.session.commit()
    print("[✓] Ozon.ru scraping přes Yandex complete.")
