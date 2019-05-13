import pika
import logging


class RabbitMQConnector:
    def __init__(self, mb_properties):
        self._mb_properties = mb_properties
        self._connection = None
        self._channel = None

    def connect(self):
        credentials = pika.PlainCredentials(
            self._mb_properties.get_username(),
            self._mb_properties.get_password()
        )
        parameters = pika.ConnectionParameters(
            host=self._mb_properties.get_host(),
            credentials=credentials
        )
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def declare_queue(self, queue_properties):
        args = dict()
        if queue_properties.get_maxpriority() > 0:
            args["x-max-priority"] = queue_properties.get_maxpriority()
        if queue_properties.get_maxqueuelength() > 0:
            args["x-max-length"] = queue_properties.get_maxqueuelength()

        res = self._channel.queue_declare(
            queue=queue_properties.get_queuename(),
            durable=queue_properties.is_durable(),
            auto_delete=queue_properties.is_autodelete(),
            passive=queue_properties.is_passive(),
            exclusive=queue_properties.is_exclusive(),
            arguments=args
        )

        logging.debug(
            "Queue has been declared: (consumers: {}, messages: {}, queue_name: {}". format(
                res.method.consumer_count,
                res.method.message_count,
                res.method.queue
            )
        )
        return res.method.consumer_count, res.method.message_count, res.method.queue

    def bind_queue(self, queue_properties, exchange_name, routing_key):
        self._channel.queue_bind(
            queue=queue_properties.get_queuename(),
            exchange=exchange_name,
            routing_key=routing_key
        )

    def unbind_queue(self, queue_properties, exchange_name, routing_key):
        self._channel.queue_unbind(
            queue=queue_properties.get_queuename(),
            exchange=exchange_name,
            routing_key=routing_key
        )

    def consume(self, queue_name, on_message_callback):
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message_callback,
            consumer_tag="eistrej-consumer-pika-0.0.1"
        )
        self._channel.start_consuming()

    def publish(self, routing_key, message):
        self._channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2, # Permanent
                priority=None
            )
        )
        print("Message published: ", message)

    def delete_queue(self, queue_name):
        try:
            self._channel.queue_delete(
                queue=queue_name,
                if_unused=True,
                if_empty=True
            )
        except Exception as e:
            (_, message) = e.args
            if message[0:19] == "PRECONDITION_FAILED":
                logging.error("The queue is used or not empty.")
            else:
                raise
            return False
        return True
