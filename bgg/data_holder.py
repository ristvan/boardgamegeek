import logging


class DataHolder:
    def add_user(self, user):
        logging.info("user: {}".format(str(user)))

    def add_player(self, player):
        logging.info("player: {}".format(str(player)))

    def add_game(self, game):
        logging.info("game: {}".format(str(game)))
