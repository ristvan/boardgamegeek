import urllib.request
import time
import logging
from bgg.data_fetcher import DataFetcher
from bgg.data_converter import DataConverter
from bgg.data_holder import DataHolder


# logging.basicConfig(level=logging.DEBUG,
#                     format='[%(levelname)s] (%(threadName)s) %(message)s')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(funcName)s - %(message)s'
)


def worker():
    logging.debug("Starting")
    time.sleep(2)
    logging.debug("Ending")


def my_service():
    logging.debug("Starting")
    time.sleep(3)
    logging.debug("Ending")


# logging.info("START")
# threads = [threading.Thread(name='my_service', target=my_service),
#            threading.Thread(name='worker', target=worker),
#            threading.Thread(target=worker)]
#
# logging.info("Starting threads")
# for thread in threads:
#     thread.start()
#
# logging.info("Waiting for threads to finish")
# for thread in threads:
#     thread.join()
#
# logging.info("EXIT")

df = DataFetcher()
dh = DataHolder()
dc = DataConverter(data_fetcher=df, data_holder=dh)
dc.convert()
