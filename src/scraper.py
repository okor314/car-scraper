import asyncio
from typing import Optional
from playwright.async_api import Page

from src.page import CatalogPage, DetailPage
from database.utils import get_db
from database.db import create_table, save_cars

BASE_URL = 'https://auto.ria.com'
START_URL = 'https://auto.ria.com/uk/search/?indexName=auto&limit=10&page={}'



class Scraper:
    def __init__(self, browser, max_pages: int = 5):
        self.browser = browser
        self.semaphore = asyncio.Semaphore(max_pages)

        self.db = get_db()
        create_table(self.db)

    async def scrape_detail_page(self, url: str):
        async with self.semaphore:
            page: Page = await self.browser.new_page()

            try:
                await page.goto(url, wait_until="domcontentloaded")
                await page.wait_for_selector('div#sellerInfo div.button-main button[data-action="showBottomPopUp"]',
                                             timeout=10_000)
                
                data = DetailPage(await page.content()).parse()

                phone = await self.fetch_phone(page)
                
                data['phone_number'] = phone

                return data
            except Exception as e:
                return None
            finally:
                await page.close()


    async def fetch_phone(self, page: Page) -> Optional[int]:
        try:
            async with page.expect_response(lambda r: "auto/popUp" in r.url, timeout=15_000) as response:
                buttons = page.locator('div#sellerInfo div.button-main button[data-action="showBottomPopUp"]')
                await buttons.nth(0).click()

            r = await response.value
            data = await r.json()
            phone_str = (
                data.get("additionalParams", {})
                    .get("phoneStr")
            )

            if not phone_str:
                return None

            phone = (
                "38" + phone_str
                    .replace(" ", "")
                    .replace("(", "")
                    .replace(")", "")
            )

            return int(phone)

        except Exception as e:
            print(f"[phone error] {page.url}: {e}")
            return None
        
    async def scrape_catalog_page(self, url: str):
        try:
            self.main_page = await self.browser.new_page()
            await self.main_page.goto(url, wait_until="domcontentloaded")

            catalog = CatalogPage(await self.main_page.content())
            links = [BASE_URL + link for link in catalog.get_URls()]

            tasks = [
                asyncio.create_task(self.scrape_detail_page(link))
                for link in links
            ]

            results = await asyncio.gather(*tasks)
            results = [r for r in results if r is not None]
            
            save_cars(results, self.db)

        except Exception as e:
            print(f"[catalog error] {url}: {e}")
        finally:
            return catalog.is_last()

    
    async def scrape(self, start_page: int = 0, max_pages: int = -1):
            page_num = start_page
            
            while True:
                url = START_URL.format(page_num)
                print(f'[scraping catalog] page = {page_num}, url: {url}')
                is_last = await self.scrape_catalog_page(url)

                if is_last:
                    break

                if max_pages != -1 and page_num - start_page >= max_pages:
                    break

                page_num += 1
        

if __name__ == '__main__':
    pass
        
