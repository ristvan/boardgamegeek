import logging


class DataHolder:
    def add_user(self, user):
        logging.debug("user: {}".format(str(user)))

    def add_player(self, player):
        logging.debug("player: {}".format(str(player)))

    def add_game(self, game):
        logging.debug("game: {}".format(str(game)))
