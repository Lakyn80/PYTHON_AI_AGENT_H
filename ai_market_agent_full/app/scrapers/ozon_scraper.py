import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from app.db import db
from app.models import Entry, Source

QUERIES = [
    "ГИАЛХОНДРО ГХ плюс",
    "глюкозамин хондроитин",
    "глюкозамин сульфат",
    "хондроитин сульфат",
    "суставы",
    "боль в суставах",
    "артрит",
    "хондропротекторы"
]

def scrape_ozon():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    source = Source.query.filter_by(name="Ozon").first()
    if not source:
        source = Source(name="Ozon", url="https://www.ozon.ru/")
        db.session.add(source)
        db.session.commit()

    total_found = 0

    for query in QUERIES:
        url = f"https://www.ozon.ru/search/?text={query}"
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        items = soup.select("div.b4a1")[:10]
        print(f"🔎 Ozon query '{query}': {len(items)} results")

        for item in items:
            title = item.get_text(strip=True)
            if not Entry.query.filter_by(title=title, source_id=source.id).first():
                entry = Entry(
                    title=title,
                    content=f"Získáno z Ozon (dotaz: {query})",
                    posted_at=datetime.utcnow(),
                    source_id=source.id
                )
                db.session.add(entry)
                total_found += 1

    db.session.commit()
    driver.quit()
    print(f"[✓] Ozon scraping complete. Total new entries added: {total_found}")
