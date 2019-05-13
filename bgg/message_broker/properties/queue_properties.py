class QueueProperties:
    def __init__(self, name, durable,
                 max_queue_length=0,
                 max_priority=0,
                 exchange_name=None,
                 binding_keys=list(),
                 passive=False):
        self._queue_name = name
        self._durable = durable
        self._auto_delete = False
        self._max_queue_length = max_queue_length
        self._max_priority = max_priority
        self._exclusive = False
        self._passive = passive
        self._exchange_name = exchange_name
        self._binding_keys = binding_keys

    def get_queue_name(self):
        return self._queue_name

    def is_durable(self):
        return self._durable

    def is_auto_delete(self):
        return self._auto_delete

    def get_max_priority(self):
        return self._max_priority

    def get_max_queue_length(self):
        return self._max_queue_length

    def is_exclusive(self):
        return self._exclusive

    def is_passive(self):
        return self._passive

    def get_exchange_name(self):
        return self._exchange_name

    def get_binding_keys(self):
        return self._binding_keys
