from huesdk import Hue
import json
import os


PREFERENCES_FILENAME = ".huebert"
DEFAULT_PREFS = dict()


def _load_prefs(filename):
    with open(os.path.join(os.path.expanduser("~"), filename), "r") as infile:
        json_text = infile.read()
        prefs = json.loads(json_text)
        return prefs


def _save_prefs(filename, prefs):
    with open(os.path.join(os.path.expanduser("~"), filename), "w") as outfile:
        json_text = json.dumps(prefs)
        outfile.write(json_text)
    return


def initialise(filename):
    try:
        prefs = _load_prefs(filename)
        return prefs
    except FileNotFoundError:
        prefs = DEFAULT_PREFS
        try:
            prefs["username"] = Hue.connect("203.44.160.215")
            print(prefs)
        except Exception as ex:
            print(f"Press Link button on hub {type(ex)} {ex}")
        _save_prefs(filename, prefs)
    return prefs


def main():
    prefs = initialise(PREFERENCES_FILENAME)
    print(prefs)
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
