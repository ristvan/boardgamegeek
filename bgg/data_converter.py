import logging
from bgg.game import Game
from bgg.player import Player
from bgg.user import User


class DataConverter:
    def __init__(self, data_fetcher, data_holder):
        self.data_fetcher = data_fetcher
        self.data_holder = data_holder

    def convert(self):
        root = self.data_fetcher.get_root()
        self.read_user(root)
        total_number_of_plays = int(root.get("total"))
        current_page = int(root.get("page"))
        self.convert_one_page(root)
        while current_page * 100 < total_number_of_plays:
            root = self.data_fetcher.get_root(page=current_page+1)
            current_page = int(root.get("page"))
            total_number_of_plays = int(root.get("total"))
            self.convert_one_page(root)

    def read_user(self, root):
        username = root.get("username")
        user_id = int(root.get("userid"))
        user = User(user_id, username)
        self.data_holder.add_user(user)

    def convert_one_page(self, root):
        plays = None
        for child in root.iter("plays"):
            plays = child
        counter = 0
        for play_node in plays.iter("play"):
            counter += 1
            game = self.read_game(play_node)
            logging.debug(str(game))
            self.read_players(play_node)
        logging.debug("number of plays = {}".format(counter))

    def read_players(self, node_of_play_item):
        for player_node in node_of_play_item.iter("player"):
            player = Player()
            player.user_id = int(player_node.get("userid"))
            player.name = player_node.get("username")
            player.play_id = int(node_of_play_item.get("id"))
            player.score = player_node.get("score")
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
