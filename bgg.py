import xml.etree.ElementTree
import urllib.request
import threading
import time
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)s) %(message)s')


class Player:
    def __init__(self):
        self.user_id = None
        self.play_id = None
        self.score = None
        self.name = None
        self.starting_position = None
        self.rating = None
        self.is_new = False
        self.is_win = False

    def __str__(self):
        return "uid={}/{}/{}/{}/{}/{}/{}/{}".format(
            self.user_id,
            self.play_id,
            self.name,
            self.score,
            self.starting_position,
            self.rating,
            self.is_new,
            self.is_win
        )


class Game:
    def __init__(self):
        self.name = None
        self.id = None

    def __str__(self):
        return "{} - {}".format(self.id, self.name)


def worker():
    logging.debug("Starting")
    time.sleep(2)
    logging.debug("Ending")


def my_service():
    logging.debug("Starting")
    time.sleep(3)
    logging.debug("Ending")


# logging.info("START")
# threads = [threading.Thread(name='my_service', target=my_service),
#            threading.Thread(name='worker', target=worker),
#            threading.Thread(target=worker)]
#
# logging.info("Starting threads")
# for thread in threads:
#     thread.start()
#
# logging.info("Waiting for threads to finish")
# for thread in threads:
#     thread.join()
#
# logging.info("EXIT")


response = urllib.request.urlopen("https://www.boardgamegeek.com/xmlapi2/plays?username=ristvan")
# raw_response = response.read()
# print(raw_response)

tree = xml.etree.ElementTree.parse(response)
root = tree.getroot()


def print_attributes(node):
    for (root_attrib_key, root_attrib_value) in node.items():
        logging.debug("{} - {}".format(root_attrib_key, root_attrib_value))


print_attributes(root)
username = root.get("username")
userid = int(root.get("userid"))
total_number_of_plays = int(root.get("total"))
current_page = int(root.get("page"))

plays = None
for child in root.iter("plays"):
    plays = child

counter = 0
for play_node in plays.iter("play"):
    print(play_node)
    print_attributes(play_node)
    counter += 1
    for game_node in play_node.iter("item"):
        game = Game()
        game.name = game_node.get("name")
        game.id = game_node.get("objectid")
    print(str(game))
    for player_node in play_node.iter("player"):
        print(player_node)
        player = Player()
        player.user_id = int(player_node.get("userid"))
        player.name = player_node.get("username")
        player.play_id = int(play_node.get("id"))
        player.score = int(player_node.get("score"))
        sp = player_node.get("startposition")
        player.starting_position = int(sp if len(sp) > 0 else "0")
        player.rating = int(player_node.get("rating"))
        is_new = bool(player_node.get("new"))
        is_win = bool(player_node.get("win"))

        print_attributes(player_node)
        print(str(player))
    break

print(counter)
