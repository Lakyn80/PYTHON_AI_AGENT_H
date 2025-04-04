from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from app.models import ProductEntry
from app.db import db
import os

def scrape_wildberries_yandex():
    url = "https://www.wildberries.ru/catalog/0/search.aspx?search=суставы"

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

    cards = soup.select("div.product-card__wrapper")

    for card in cards[:20]:
        try:
            title_elem = card.select_one("span.goods-name")
            href_elem = card.select_one("a")

            if not title_elem or not href_elem:
                continue

            title = title_elem.get_text(strip=True)
            href = href_elem.get("href")
            product_url = f"https://www.wildberries.ru{href}"

            product = ProductEntry(
                platform="wildberries",
                title=title,
                product_url=product_url
            )
            db.session.add(product)

        except Exception as e:
            print("Wildberries Yandex error:", e)

    db.session.commit()
    print("[✓] Wildberries scraping přes Yandex complete.")
