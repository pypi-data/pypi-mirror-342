"""ticker lists"""

import json
from pathlib import Path

from .config import BARDATA_FOLDER



def get_tickers(name):
    """list of tickers of given name"""

    list_folder = Path(BARDATA_FOLDER, "ticker-lists").expanduser()

    path = list_folder.joinpath(f"{name}.json")

    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist")

    with open(path, "r") as f:
        tickers = json.load(f)

    return tickers


def ticker_lists():
    """ticker list names"""

    list_folder = Path(BARDATA_FOLDER, "ticker-lists").expanduser()

    names = [
        name.stem
        for name in list_folder.glob("*.json")
    ]

    return names
