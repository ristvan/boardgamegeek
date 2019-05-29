from queue import Queue


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
