import xml.etree.ElementTree
import urllib.request


class DataFetcher:
    def get_root(self, page=1):
        page
        xml_lines = [
            '<plays username="ristvan" userid="247009" total="2" page="1" termsofuse="https://boardgamegeek.com/xmlapi/termsofuse">',
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
            '    <play id = "24924689" date = "2017-09-03" quantity = "1" length = "0" incomplete = "0" nowinstats = "0" location = "Atiék">',
            '        <item name = "Power Grid (Recharged Version)" objecttype = "thing" objectid = "2651">',
            '            <subtypes>',
            '                <subtype value = "boardgame" />',
            '                <subtype value = "boardgameimplementation" />',
            '            </subtypes>',
            '        </item>',
            '        <players>',
            '            <player username="Lujzi" userid="241629" name="Lujzi" startposition="1" color="Yellow" score="14" new = "0" rating = "0" win = "0"/>',
            '            <player username="Yamamoto" userid="86718" name="Kristóf" startposition="2" color="Green" score="13" new="0" rating="0" win="0"/>',
            '            <player username="Detti76" userid="237335" name="Detti" startposition="3" color="Purple" score="15 (150)" new="0" rating="0" win="0"/>',
            '            <player username="ristvan" userid="247009" name="Isti" startposition="4" color="Blue" score="15 (165)" new="0" rating="0" win="0"/>',
            '            <player username="Atimati" userid="236336" name="Ati" startposition="5" color="Red" score="15 (257)" new="0" rating="0" win="1"/>',
            '        </players>',
            '    </play>',
            '</plays>'
        ]

        return xml.etree.ElementTree.fromstringlist(xml_lines)


class BGGDataFetcher:
    def __init__(self, endpoint="plays", user="ristvan"):
        self.endpoint = endpoint
        self.user = user

    def get_root(self, page=1):
        bgg_api_url = "https://www.boardgamegeek.com/xmlapi2"
        url_format = "{rest_api_url}/{endpoint}?{parameters}"
        url = url_format.format(
            rest_api_url=bgg_api_url,
            endpoint=self.endpoint,
            parameters="username={}&page={}".format(self.user, page)
        )
        response = urllib.request.urlopen(url)
        tree = xml.etree.ElementTree.parse(response)
        return tree.getroot()
