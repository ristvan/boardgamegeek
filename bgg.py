import xml.etree.ElementTree
import urllib.request
import threading
import time
import logging

from bgg.player import Player

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)s) %(message)s')

class Game:
    def __init__(self):
        self.name = None
        self.id = None

    def __str__(self):
        return "(Game)id={} - name={}".format(self.id, self.name)


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

def bgg_getter_function():
    BGG_API_URL = "https://www.boardgamegeek.com/xmlapi2"
    url_format = "{rest_api_url}/{endpoint}?{parameters}"
    url = url_format.format(
        rest_api_url=BGG_API_URL,
        endpoint="plays",
        parameters="username=ristvan"
    )
    response = urllib.request.urlopen(url)
    return response


xml_lines = [
    '<plays username="ristvan" userid="247009" total="2039" page="1" termsofuse="https://boardgamegeek.com/xmlapi/termsofuse">',
    '    <play id="33070661" date="2019-01-05" quantity="1" length="0" incomplete="0" nowinstats="0" location="Otthon">',
    '        <item name="Sanssouci" objecttype="thing" objectid="146816">',
    '            <subtypes>',
    '                <subtype value="boardgame"/>',
    '            </subtypes>',
    '        </item>',
    '        <players>',
    '            <player username="Detti76" userid="237335" name="Detti" startposition="1" color="Red" score="86" new="0" rating="0" win="0"/>',
    '            <player username="ristvan" userid="247009" name="Isti" startposition="2" color="Blue" score="89" new="0" rating="0" win="1"/>',
    '        </players>',
    '    </play>',
    '    <play id="33038839" date="2019-01-04" quantity="1" length="0" incomplete="0" nowinstats="0" location="Dundánál">',
    '        <item name="Gùgōng" objecttype="thing" objectid="250458">',
    '            <subtypes>',
    '                <subtype value="boardgame"/>',
    '            </subtypes>',
    '        </item>',
    '        <players>',
    '            <player username="Dunda" userid="124020" name="Dunda" startposition="1" color="Orange" score="28" new="0" rating="0" win="0"/>',
    '            <player username="Detti76" userid="237335" name="Detti" startposition="2" color="Pink" score="35" new="0" rating="0" win="0"/>',
    '            <player username="ristvan" userid="247009" name="Isti" startposition="3" color="Red" score="48" new="0" rating="0" win="1"/>',
    '            <player username="PZS69" userid="442494" name="PZs" startposition="4" color="Blue" score="32" new="0" rating="0" win="0"/>',
    '        </players>',
    '    </play>',
    '</plays>'
]

# tree = xml.etree.ElementTree.parse(bgg_getter_function())
# root = tree.getroot()
root = xml.etree.ElementTree.fromstringlist(xml_lines)


def print_attributes(node):
    for (root_attrib_key, root_attrib_value) in node.items():
        logging.debug("{} - {}".format(root_attrib_key, root_attrib_value))


username = root.get("username")
userid = int(root.get("userid"))
total_number_of_plays = int(root.get("total"))
current_page = int(root.get("page"))

plays = None
for child in root.iter("plays"):
    plays = child

counter = 0
for play_node in plays.iter("play"):
    print_attributes(play_node)
    counter += 1
    for game_node in play_node.iter("item"):
        game = Game()
        game.name = game_node.get("name")
        game.id = game_node.get("objectid")
    logging.info(str(game))
    players = list()
    for player_node in play_node.iter("player"):
        player = Player()
        player.user_id = int(player_node.get("userid"))
        player.name = player_node.get("username")
        player.play_id = int(play_node.get("id"))
        player.score = int(player_node.get("score"))
        sp = player_node.get("startposition")
        player.starting_position = int(sp if len(sp) > 0 else "0")
        player.color = player_node.get("color")
        player.rating = int(player_node.get("rating"))
        player.is_new = bool(int(player_node.get("new")))
        player.is_win = bool(int(player_node.get("win")))

        # print_attributes(player_node)
        players.append(str(player))
    break
logging.info(str(players))

logging.debug("number of plays = {}".format(counter))
