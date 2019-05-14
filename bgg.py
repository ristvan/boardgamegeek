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
    def __init__(self, name=None, communication_channel_factory=None):
        threading.Thread.__init__(
            self,
            # group=group,
            # target=target,
            name=name,
            # verbose=verbose
        )
        self._communication_channel_factory = communication_channel_factory

    def run(self) -> None:
        data_converter = DataConverter(
            data_fetcher=DataFetcher(),
            data_holder=DataHolder(data_storage_factory=self._communication_channel_factory)
        )
        data_converter.convert()
        queue = self._communication_channel_factory.create_communication_channel()
        queue.send("QUIT")
        logging.debug("Messages are sent")


class DataStorageThread(threading.Thread):
    def __init__(self, name=None, communication_channel_factory=None):
        threading.Thread.__init__(
            self,
            name=name,
        )
        self._queue = communication_channel_factory.create_communication_channel()

    def run(self) -> None:
        logging.info("Start")
        while True:
            h = self._queue.get()
            logging.debug(str(h))
            if h == "QUIT":
                break
        logging.info("Finish")


class CommunicationChannelFactory:
    _communication_channel = None

    class QueueWrapper:
        def __init__(self):
            self.queue = Queue(maxsize=1)

        def send(self, message):
            self.queue.put(message)

        def get(self):
            return self.queue.get()

    def create_communication_channel(self):
        if self._communication_channel is None:
            self._communication_channel = CommunicationChannelFactory.QueueWrapper()
        return self._communication_channel


if __name__ == "__main__":
    logging.info("START")

    ccf = CommunicationChannelFactory()

    data_collector_thread: DataCollectorThread = DataCollectorThread(
        name="DataCollector",
        communication_channel_factory=ccf
    )
    data_collector_thread.start()

    data_storage_thread: DataStorageThread = DataStorageThread(
        name="DataStorage",
        communication_channel_factory=ccf
    )
    data_storage_thread.start()

    main_thread = threading.currentThread()
    for thread in threading.enumerate():
        if thread is not main_thread:
            thread.join()

    logging.info("EXIT")
