import json

from typing import Dict, Any
from functools import partial

from bs4 import BeautifulSoup

from src.utils import catch_errors

class CatalogPage:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_URls(self) -> list[str]:
        """Returns relative links to product pages"""

        products = self.soup.select('a[class~="product-card"]')
        return [product.get('href') for product in products]
    
    def is_last(self) -> bool:
        disabled_button = self.soup.select_one('button[title="Next"][disabled]')
        return bool(disabled_button)
    
class DetailPage():
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

        self.selectors = {
            'url':          'link[rel="canonical"]',
            'title':        'h1[class*="title"]',
            'price_usd':    'script[type="application/ld+json"]:contains("price")',
            'odometer':     'script[type="application/ld+json"]:contains("price")',
            'username':     'div#sellerInfoUserName span',
            'image_url':    'picture img',
            'images_count': 'div#photoSlider span.common-badge span:last-child',
            'car_number':   'div.car-number span',
            'car_vin':      'div#badgesVinGrid',
        }

        self.extractors = {
            'url':          lambda tag: tag.get('href'),
            'title':        lambda tag: tag.text.strip(),
            'price_usd':    lambda tag: json.loads(tag.text).get('offers').get('price'),
            'odometer':     lambda tag: json.loads(tag.text).get('mileageFromOdometer').get('value'),
            'username':     lambda tag: tag.text.strip(),
            'image_url':    lambda tag: tag.get('data-src'),
            'images_count': lambda tag: int(tag.text.strip()),
            'car_number':   lambda tag: tag.text.strip(),
            'car_vin':      lambda tag: tag.text.strip(),
        }

        self.default_values = {}

    def parse(self) -> Dict[str, Any]:
        """Parce datail page of product and return dictionary
        with product data."""

        # Modifying extarctor funcs to return default value
        # if error occurs
        extractors = {key: partial(catch_errors, 
                                   extr, 
                                   lambda _: self.default_values.get(key)) 
                      for key, extr in self.extractors.items()
                      }
        result = {
            key: extractors[key](self.soup.select_one(selector)) 
            for key, selector in self.selectors.items()
        }

        return result

        


if __name__ == '__main__':
    pass
        
        

