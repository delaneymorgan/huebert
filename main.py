import argparse
from huesdk import Hue
import json
import os
import random
import time


PREFERENCES_FILENAME = ".huebert"
BRIDGE_IP_ADDRESS = "203.44.160.215"
DEFAULT_PREFS = dict()
__version__ = "1.0.1"


class Huebert(object):
    def __init__(self, args):
        self.args = args
        self.initialise()
        return

    def _load_prefs(self):
        with open(os.path.join(os.path.expanduser("~"), self.args.prefs), "r") as infile:
            json_text = infile.read()
            self.prefs = json.loads(json_text)
            return

    def _save_prefs(self):
        with open(os.path.join(os.path.expanduser("~"),self.args.prefs), "w") as outfile:
            json_text = json.dumps(self.prefs)
            outfile.write(json_text)
        return

    def initialise(self):
        while True:
            try:
                self._load_prefs()
                self.hue = Hue(bridge_ip=self.prefs["bridge"], username=self.prefs["username"])
                return
            except FileNotFoundError:
                self.prefs = DEFAULT_PREFS
                self.prefs["bridge"] = self.args.bridge
                try:
                    self.prefs["username"] = Hue.connect(self.args.bridge)
                except Exception as ex:
                    print(f"Press Link button on hub {type(ex)} {ex}")
                self._save_prefs()

    def get_hue(self):
        return self.hue


def arg_parser():
    """
    parse arguments

    :return: the parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Huebert.')
    parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")
    parser.add_argument("-d", "--diagnostic", help="diagnostic mode (includes verbose)", action="store_true")
    parser.add_argument("-b", "--bridge", help="Hue Bridge address", default=BRIDGE_IP_ADDRESS)
    parser.add_argument("-p", "--prefs", help="preferences file", default=PREFERENCES_FILENAME)
    parser.add_argument("--version", action="version", version='%(prog)s {version}'.format(version=__version__))
    args = parser.parse_args()
    return args

def main():
    args = arg_parser()
    huebert = Huebert(args)
    hue = huebert.get_hue()
    lights = hue.get_lights()
    for light in lights:
        print(light.name)
        print(light.id_)
        print(light.is_on)
        print(light.bri)  # Brightness from 1 to 254
        print(light.hue)  # the color with a value between 0 and 65535
        print(light.sat)  # Saturation from 1 to 254
        print("---------")

    for i in range(1000):
        for light in lights:
            light.on()
            color = "#%06x" % random.randrange(0, 0xffffff)
            light.set_color(hexa=color)
            time.sleep(0.25)
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
