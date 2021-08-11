import os

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
PRODUCT_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'products.json')
CHECK_FREQUENCY = 60 * 60 * 1  # every 6 hours
