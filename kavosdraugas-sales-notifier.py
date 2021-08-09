import time
import sys

from core.products import Products
from core import config


if __name__ == '__main__':
    try:
        products = Products.from_file()

        while True:
            products_to_notify = products.get_products_to_notify()

            for product in products_to_notify:
                product.notify()
                time.sleep(5)

            products.to_file()

            time.sleep(config.CHECK_FREQUENCY)
    except KeyboardInterrupt:
        print('Closing...')
        sys.exit(0)
