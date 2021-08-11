from dataclasses import dataclass, field
from typing import List

from datetime import datetime
import time
import json
import os

from bs4 import BeautifulSoup
import requests

from core import config


@dataclass()
class Product:
    url: str
    on_sale: bool = False
    name: str = None
    price: float = None
    last_checked_on: datetime = None

    def get_new_data(self):
        """
        Gets product data from ecommerce site and parses it
        :return:
            bool(sale_attribute) (bool):                     is product on sale
            float(price_attribute.attrs['content']) (float): product price
            name_attribute.text (str):                       name of a product
        """

        page = requests.get(self.url,
                            headers={'User-Agent': config.USER_AGENT})

        soup = BeautifulSoup(page.text, 'html.parser')
        sale_attribute = soup.select_one('div.single-product__price.sale')

        price_attribute = soup.find('span', attrs={'itemprop': 'price'})
        name_attribute = soup.select_one('h1.single-product__title')

        return bool(sale_attribute), float(price_attribute.attrs['content']), name_attribute.text

    def update(self, **kwargs):
        """
        Updates product attributes with new data
        """

        self.on_sale = kwargs.get('on_sale', self.on_sale)
        self.price = kwargs.get('price', self.price)
        self.last_checked_on = datetime.now()
        self.name = kwargs.get('name', self.name)

    def need_to_notify(self, need_update=True):
        """
        Checks if product is on sale and needs to send the notification
        :param need_update: if true calls update() method and updates the product data
        :return:
            need_to_notify (bool): is product on sale and need to notify or not
        """

        need_to_notify = False
        on_sale, price, name = self.get_new_data()

        # fancy logic to not notify multiple times and if new price is not lower current
        if self.on_sale != on_sale and on_sale:
            need_to_notify = True
        elif self.on_sale == on_sale and on_sale and self.price and price < self.price:
            need_to_notify = True

        if need_update:
            self.update(on_sale=on_sale, price=price, name=name)

        return need_to_notify

    def notify(self):
        """
        Send notification to screen
        """

        title = 'Kavosdraugas sale!'
        command = f'''
                    osascript -e 'display notification "{self.name}" with title "{title}"'
                    '''
        os.system(command)

    def as_dict(self):
        """
        Returns object as dictionary
        """

        return {
            'url': self.url,
            'on_sale': self.on_sale,
            'last_checked_on': self.last_checked_on.strftime('%Y-%m-%d %H:%M:%S'),
            'price': self.price,
            'name': self.name
        }


@dataclass()
class Products:
    products: List[Product] = field(default_factory=list)

    def check_and_notify(self):
        """
        Checks if products are on sale and notifies
        """

        for product in self.products:
            if product.need_to_notify():
                product.notify()
                time.sleep(5)

    @classmethod
    def from_file(cls, file_path=config.PRODUCT_FILE_PATH):
        """
        Loads products file
        :param file_path: path of product file
        :return: Products class instance
        """

        with open(file_path) as products_file:
            products = json.load(products_file)

            products_buffer = []

            for product in products:
                p = Product(url=product['url'],
                            on_sale=product.get('on_sale', None),
                            name=product.get('name', None),
                            price=product.get('price', None),
                            last_checked_on=datetime.strptime(product['last_checked_on'], '%Y-%m-%d %H:%M:%S') if product.get('last_checked_on', None) else None)

                products_buffer.append(p)

            return cls(products=products_buffer)

    def to_file(self, file_path=config.PRODUCT_FILE_PATH):
        """
        Saves products data into file
        :param file_path: path of product file
        """

        with open(file_path, 'w') as products_file:
            json.dump(self.as_dict(), products_file, indent=4)

    def as_dict(self):
        """
        Returns object as dictionary
        """

        return [product.as_dict() for product in self.products]
