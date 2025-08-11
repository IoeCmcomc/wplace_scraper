import asyncio
import aiohttp
import pickle
from os import makedirs, listdir
from os.path import join, exists
from email.utils import parsedate_tz, mktime_tz, formatdate
from time import sleep

CONCURRENT_REQUESTS = 5 # Maximum number of simultaneous requests
SLEEP_TIME = 1 # number of seconds to wait after a successful (200 or 404) request
SLEEP_TIME_429 = 5 # number of seconds to wait before retrying when getting a 429
CACHE_FILENAME = "modified_since_cache.pkl"
MAX_X = 2047
MAX_Y = 137

in_url = lambda x, y: "https://backend.wplace.live/files/s0/tiles/" + str(x) + "/" + str(y) + ".png"
out_dir = lambda x, y: join("files", "s0", "tiles", str(x), str(y))
out_path = lambda x, y, last_modified: join(out_dir(x, y), str(last_modified) + ".png")

def make_wplace_dirs():
    for x in range(MAX_X + 1):
        for y in range(MAX_Y + 1):
            makedirs(join("files", "s0", "tiles", str(x), str(y)), exist_ok=True)

async def get_tile(x, y, session, since, sem):
    retry = True
    async with sem:
        while retry:
            headers = {}
            if (x in since and y in since[x]):
                headers['If-Modified-Since'] = formatdate(since[x][y], usegmt=True)
            else:
                since[x] = {}
                # check if file already downloaded
                dir = out_dir(x, y)
                if exists(dir):
                    # find highest timestamp in dir and use that
                    files = sorted(listdir(dir))
                    if len(files) != 0:
                        if files[-1] == ".DS_Store": del files[-1] # ugh
                        if len(files) != 0:
                            since[x][y] = int(files[-1].replace(".png", ""))
                            headers['If-Modified-Since'] = formatdate(since[x][y], usegmt=True)
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
                    print("429: sleeping", SLEEP_TIME_429, "seconds")
                    await asyncio.sleep(SLEEP_TIME_429)
                elif resp.status != 200:
                    print("got status", resp.status, "on tile", x, y)
                    retry = False
                    return
                else:
                    # convert Last-Modified to a unix timestamp
                    timestamp = mktime_tz(parsedate_tz(resp.headers['Last-Modified']))
                    since[x][y] = timestamp
                    with open(out_path(x, y, timestamp), "wb") as f:
                        f.write(await resp.content.read())
                    print("saved tile", x, y)
                    retry = False
                    await asyncio.sleep(SLEEP_TIME)

async def main():
    sem = asyncio.Semaphore(CONCURRENT_REQUESTS)
    if not exists("files"): make_wplace_dirs()
    if exists(CACHE_FILENAME):
        with open(CACHE_FILENAME, "rb") as f: since = pickle.load(f)
    else:
        since = {}
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as grp:
            for x in range(MAX_X + 1):
                for y in range(MAX_Y + 1):
                    grp.create_task(get_tile(x, y, session, since, sem))
            print("tasks created")
    with open(CACHE_FILENAME, "wb") as f: pickle.dump(since, f)

if __name__ == "__main__":
    asyncio.run(main())
