PIXEL_TILE_URL_PATTERN = "https://backend.wplace.live/files/s0/tiles/{x}/{y}.png"
# PIXEL_TILE_URL_PATTERN = "https://openplace.live/files/s0/tiles/{x}/{y}.png"

CONCURRENT_REQUESTS = 5 # Maximum number of simultaneous requests
SLEEP_TIME = 1 # number of seconds to wait after a successful (200 or 404) request
SLEEP_TIME_429 = 5 # number of seconds to wait before retrying when getting a 429
CACHE_FILENAME = "modified_since_cache.pkl"
FROM_X = 1600
FROM_Y = 885
TO_X = 1700
TO_Y = 990

MAX_X = 2047
MAX_Y = 137

TILES_FOLDER = 'tiles'
