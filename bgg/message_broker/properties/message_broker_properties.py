class MessageBrokerProperties:
    def __init__(self, host, port=5672, username="guest", password="guest"):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    def get_host(self):
        return self._host

    def get_port(self):
        return self._port

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password
