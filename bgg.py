import logging
from bgg.data_fetcher import DataFetcher
from bgg.data_converter import DataConverter
from bgg.data_holder import DataHolder

import threading
from queue import Queue

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(threadName)s) %(funcName)s - %(message)s'
)


class DataCollectorThread(threading.Thread):
    def __init__(self, name=None, queue=None):
        threading.Thread.__init__(
            self,
            # group=group,
            # target=target,
            name=name,
            # verbose=verbose
        )
        self._queue = queue

    def run(self) -> None:
        data_converter = DataConverter(
            data_fetcher=DataFetcher(),
            data_holder=DataHolder()
        )
        data_converter.convert()
        self._queue.put("hello")
        self._queue.put("world")
        self._queue.put("fasfa")
        self._queue.put("QUIT")
        logging.debug("Messages are sent")


class DataStorageThread(threading.Thread):
    def __init__(self, name=None, queue=None):
        threading.Thread.__init__(
            self,
            name=name,
        )
        self._queue = queue

    def run(self) -> None:
        logging.info("Start")
        while True:
            h = self._queue.get()
            logging.debug(str(h))
            if h == "QUIT":
                break
        logging.info("Finish")


if __name__ == "__main__":
    logging.info("START")

    cq = Queue(maxsize=1)

    data_collector_thread: DataCollectorThread = DataCollectorThread(name="DataCollector", queue=cq)
    data_collector_thread.start()

    data_storage_thread: DataStorageThread = DataStorageThread(name="DataStorage", queue=cq)
    data_storage_thread.start()

    main_thread = threading.currentThread()
    for thread in threading.enumerate():
        if thread is not main_thread:
            thread.join()

    logging.info("EXIT")
