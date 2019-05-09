import logging
from bgg.game import Game
from bgg.player import Player


class DataConverter:
    def __init__(self, data_fetcher, data_holder):
        self.data_fetcher = data_fetcher
        self.data_holder = data_holder

    def covert(self):
        root = self.data_fetcher.get_root()
        username = root.get("username")
        userid = int(root.get("userid"))
        total_number_of_plays = int(root.get("total"))
        current_page = int(root.get("page"))

        plays = None
        for child in root.iter("plays"):
            plays = child

        counter = 0
        for play_node in plays.iter("play"):
            self.print_attributes(play_node)
            counter += 1
            game = self.read_game(play_node)
            logging.info(str(game))
            self.read_players(play_node)
            break

        logging.debug("number of plays = {}".format(counter))

    def read_players(self, node_of_play_item):
        for player_node in node_of_play_item.iter("player"):
            player = Player()
            player.user_id = int(player_node.get("userid"))
            player.name = player_node.get("username")
            player.play_id = int(node_of_play_item.get("id"))
            player.score = int(player_node.get("score"))
            sp = player_node.get("startposition")
            player.starting_position = int(sp if len(sp) > 0 else "0")
            player.color = player_node.get("color")
            player.rating = int(player_node.get("rating"))
            player.is_new = bool(int(player_node.get("new")))
            player.is_win = bool(int(player_node.get("win")))

            self.data_holder.add_player(player)

    def read_game(self, play_node):
        result_game = Game()
        for game_node in play_node.iter("item"):
            result_game.name = game_node.get("name")
            result_game.id = game_node.get("objectid")
        self.data_holder.add_game(result_game)
        return result_game

    def print_attributes(self, node):
        for (root_attrib_key, root_attrib_value) in node.items():
            logging.debug("{} - {}".format(root_attrib_key, root_attrib_value))
