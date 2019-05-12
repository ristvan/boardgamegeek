import time
import logging
from bgg.data_fetcher import DataFetcher
from bgg.data_converter import DataConverter
from bgg.data_holder import DataHolder

import threading

# logging.basicConfig(level=logging.DEBUG,
#                     format='[%(levelname)s] (%(threadName)s) %(message)s')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(threadName)s) %(funcName)s - %(message)s'
)


class MyThread(threading.Thread):
    def run(self) -> None:
        df = DataFetcher()
        dh = DataHolder()
        dc = DataConverter(data_fetcher=df, data_holder=dh)
        dc.convert()


logging.info("START")

thr = MyThread()
thr.start()

main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()

logging.info("EXIT")
