import logging
from bgg.data_fetcher import DataFetcher
from bgg.data_converter import DataConverter
from bgg.data_holder import DataHolder

import threading

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(threadName)s) %(funcName)s - %(message)s'
)


class DataCollectorThread(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__(
            self,
            # group=group,
            # target=target,
            name=name,
            # verbose=verbose
        )

    def run(self) -> None:
        data_converter = DataConverter(
            data_fetcher=DataFetcher(),
            data_holder=DataHolder()
        )
        data_converter.convert()


class DataStorageThread(threading.Thread):
    def __init__(self, name=None):
        threading.Thread.__init__(
            self,
            name=name,
        )

    def run(self) -> None:
        logging.info("Running")


if __name__ == "__main__":
    logging.info("START")

    data_collector_thread: DataCollectorThread = DataCollectorThread(name="DataCollector")
    data_collector_thread.start()

    data_storage_thread: DataStorageThread = DataStorageThread(name="DataStorage")
    data_storage_thread.start()

    main_thread = threading.currentThread()
    for thread in threading.enumerate():
        if thread is not main_thread:
            thread.join()

    logging.info("EXIT")
