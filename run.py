import sys
import os

# Přidáme kořenovou složku projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ai_market_agent_full')))

from ai_market_agent_full.app import create_app
from ai_market_agent_full.app.routes.search_routes import search_bp

from ai_market_agent_full.app.scrapers.ozon_yandex import scrape_ozon_yandex
from ai_market_agent_full.app.scrapers.wildberries_yandex import scrape_wildberries_yandex
from ai_market_agent_full.app.scrapers.apteka_yandex import scrape_apteka_yandex

app = create_app()

# Registrace blueprintů
app.register_blueprint(search_bp)

# CLI režim – Yandex scraping only
if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]

        with app.app_context():
            if command == 'scrape-yandex':
                print("🟡 Scraping Ozon přes Yandex...")
                scrape_ozon_yandex()

                print("🟣 Scraping Wildberries přes Yandex...")
                scrape_wildberries_yandex()

                print("🔵 Scraping Apteka.ru přes Yandex...")
                scrape_apteka_yandex()

                print("✅ Yandex scraping dokončen.")
            else:
                print(f"❌ Neznámý příkaz: {command}")
                print("Použij:\n  python run.py scrape-yandex")

    else:
        app.run(debug=True)
