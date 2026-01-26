import asyncio
import aiohttp
import pickle
from os import makedirs, listdir
from os.path import join, exists
from email.utils import parsedate_tz, mktime_tz, formatdate
from time import sleep
from PIL import Image
from datetime import date
from io import BytesIO
from remove_redudant_tiles import remove_redudant_tiles
from generate_tile_availability import generate_tile_availability

from config import *

today_date = date.today().strftime("%Y%m%d")
in_url = lambda x, y: "https://backend.wplace.live/files/s0/tiles/" + str(x) + "/" + str(y) + ".png"
out_curr_path = lambda x, y: join(TILES_FOLDER, today_date, str(x), str(y) + ".webp")

def make_wplace_dirs():
    for x in range(FROM_X, TO_X + 1):
        for y in range(FROM_Y, TO_Y + 1):
            makedirs(join(TILES_FOLDER, today_date, str(x)), exist_ok=True)

async def get_tile(x: int, y: int, session: aiohttp.ClientSession, since: dict, sem: asyncio.Semaphore):
    # if x < 1675:
        # return
    # elif x == 1703 and y < 975:
    #     return
    retry = True
    async with sem:
        while retry:
            headers = {}
            if (x in since and y in since[x]):
                headers['If-Modified-Since'] = formatdate(since[x][y], usegmt=True)
            else:
                since[x] = {}
            # check if file already downloaded
            path = out_curr_path(x, y)
            if exists(path):
                print("skipped existing tile", x, y)
                return
            async with session.get(in_url(x, y), headers=headers) as resp:
                if resp.status == 404:
                    # nonexistent tile (tiles are only generated when someone places a pixel on them)
                    print("404'D on tile", x, y)
                    retry = False
                    await asyncio.sleep(SLEEP_TIME)
                    return
                elif resp.status == 304: # Not Modified
                    print("tile", x, y, "not modified")
                    retry = False
                    return
                elif resp.status == 429: # Too Many Requests
                    sleep_seconds = SLEEP_TIME_429
                    if 'Retry-After' in resp.headers:
                        sleep_seconds = int(resp.headers['Retry-After'])
                    print("429: sleeping", sleep_seconds, "seconds")
                    await asyncio.sleep(sleep_seconds)
                elif resp.status != 200:
                    print("got status", resp.status, "on tile", x, y)
                    retry = False
                    return
                else:
                    # convert Last-Modified to a unix timestamp
                    timestamp = mktime_tz(parsedate_tz(resp.headers['Last-Modified']))
                    since[x][y] = timestamp
                    content = await resp.content.read()
                    img = Image.open(BytesIO(content))
                    img.save(out_curr_path(x, y), "webp", lossless=True)
                    print("saved tile", x, y)
                    retry = False
                    await asyncio.sleep(SLEEP_TIME)

async def main():
    sem = asyncio.Semaphore(CONCURRENT_REQUESTS)
    make_wplace_dirs()
    if exists(CACHE_FILENAME):
        with open(CACHE_FILENAME, "rb") as f: since = pickle.load(f)
    else:
        since = {}
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as grp:
            for x in range(FROM_X, TO_X + 1):
                for y in range(FROM_Y, TO_Y + 1):
                    grp.create_task(get_tile(x, y, session, since, sem))
            print("tasks created")
    with open(CACHE_FILENAME, "wb") as f: pickle.dump(since, f)
    remove_redudant_tiles(f'./{TILES_FOLDER}')
    generate_tile_availability(f'./{TILES_FOLDER}')

if __name__ == "__main__":
    asyncio.run(main())