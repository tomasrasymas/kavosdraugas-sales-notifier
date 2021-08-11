import time
import sys

from core.products import Products
from core import config


if __name__ == '__main__':
    try:
        products = Products.from_file()

        while True:
            products.check_and_notify()
            products.to_file()

            time.sleep(config.CHECK_FREQUENCY)
    except KeyboardInterrupt:
        print('Closing...')
        sys.exit(0)
