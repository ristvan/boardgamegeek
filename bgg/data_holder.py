import logging


class DataHolder:
    def __init__(self, data_storage_factory=None):
        self._data_storage = data_storage_factory.create_communication_channel()

    def add_user(self, user):
        logging.info("User: {}".format(str(user)))
        self._data_storage.send(str(user))

    def add_player(self, player):
        logging.info("Player: {}".format(str(player)))
        self._data_storage.send(str(player))

    def add_game(self, game):
        logging.info("Game: {}".format(str(game)))
        self._data_storage.send(str(game))
