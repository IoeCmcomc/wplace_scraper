from os import remove, path
from datetime import date as dt_date, datetime
from datetime import timedelta
from os.path import getsize
from typing import ClassVar
from functools import cache, cached_property
from dataclasses import dataclass
from xxhash import xxh64

from config import *

# Source: https://gist.github.com/tfeldmann/fc875e6630d11f2256e746f67a09c1ae
def chunk_reader(fobj, chunk_size=1024):
    """ Generator that reads a file in chunks of bytes """
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

@dataclass(frozen=True)
class File:
    path: str

    partial_hash_count: ClassVar[int] = 0
    size_count: ClassVar[int] = 0
    data_count: ClassVar[int] = 0
    
    @classmethod
    @cache
    # Adapted from: https://gist.github.com/tfeldmann/fc875e6630d11f2256e746f67a09c1ae
    def __hash_from_path(cls, path) -> int:
        # print(f"hashing {path}")
        hashobj = xxh64()
        if path:
            with open(path, "rb") as f:
                for chunk in chunk_reader(f):
                    hashobj.update(chunk)
        return hashobj.intdigest()

    def __hash__(self) -> int:
        return self.__hash_from_path(self.path)
    
    @cached_property
    def partial_hash(self) -> int:
        self.__class__.partial_hash_count += 1
        hashobj = xxh64()
        if self.path:
            with open(self.path, "rb") as f:
                head_part = f.read(2048)
                hashobj.update(head_part)
        return hashobj.digest()
    
    @cached_property
    def data(self) -> bytes:
        self.__class__.data_count += 1

        result = bytes()
        if self.path:
            with open(self.path, "rb") as f:
                result = f.read()
        
        return result
    
    @cached_property
    def size(self) -> int:
        self.__class__.size_count += 1
        return getsize(self.path)
    
    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        assert isinstance(other, File)
        if other is self:
            return True
        if self.size != other.size:
            return False
        elif self.partial_hash != other.partial_hash:
            return False
        return self.data == other.data
    
    def __lt__(self, other) -> bool:
        assert isinstance(other, File)
        return self.path > other.path

def daterange(start_date: dt_date, end_date: dt_date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

def remove_redudant_tiles(directory):
    count = 0
    for x in range(FROM_X, TO_X + 1):
        for y in range(FROM_Y, TO_Y + 1):
            mark_file = None
            start_date = datetime(2025, 8-1, 18)
            for date in daterange(start_date, datetime.now()):
                date_string = date.strftime("%Y%m%d")
                file_path = path.normpath(path.join(directory, date_string, str(x), f'{str(y)}.webp'))
                if path.exists(file_path):
                    file = File(file_path)
                    if file == mark_file:
                        remove(file_path)
                        # print(f"Removing {file_path}")
                        count += 1
                    else:
                        mark_file = file
    print(f"Deleted {count} tiles.")

if __name__ == "__main__":
    directory = TILES_FOLDER
    remove_redudant_tiles(directory)