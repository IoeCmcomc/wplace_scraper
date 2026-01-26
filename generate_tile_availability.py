from json import dump, dumps
from os import listdir, path

from config import *

data: dict[int, dict[int, list[str]]] = {}


def get_available_dates(directory: str, x: int, y: int, all_dates: list[str]):
    results: list[str] = []
    for date in sorted(all_dates):
        if path.exists(path.join(directory, date, str(x), f"{str(y)}.webp")):
            results.append(date)
    return results


def generate_tile_availability(directory: str) -> None:
    tile_folders = [f for f in listdir(directory) if f.isdigit()]

    for x in range(FROM_X, TO_X + 1):
        data[x] = {}
        for y in range(FROM_Y, TO_Y + 1):
            date_strings = get_available_dates(directory, x, y, tile_folders)
            assert len(set(date_strings)) == len(date_strings), (
                "Duplicate dates found even after using modification times"
            )
            data[x][y] = date_strings

    dump(data, open("tile_availability.json", "w"), indent=4)
    # generate js file
    with open("tile_availability.js", "w") as js_file:
        _ = js_file.write("const tileAvailability = " + dumps(data) + ";\n")


if __name__ == "__main__":
    generate_tile_availability(TILES_FOLDER)
