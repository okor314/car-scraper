import asyncio
from src.playwright_client import PlaywrightClient
from src.scraper import Scraper

DETAIL_URLS = [
    "https://auto.ria.com/uk/auto_audi_q5_39220551.html",
    "https://auto.ria.com/uk/auto_mercedes-benz_g-class_37774969.html",
]

async def main():
    pw = PlaywrightClient()
    await pw.start()

    scraper = Scraper(
        pw.browser,
        max_pages=5
    )


    await scraper.scrape(max_pages=2)

    scraper.db.close()
    await pw.stop()

if __name__ == "__main__":
    asyncio.run(main())
