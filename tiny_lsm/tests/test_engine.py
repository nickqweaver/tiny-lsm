import glob
import os

import pytest
from tiny_lsm.engine import Engine


@pytest.fixture(autouse=True)
def clean_directory():
    target_dir = "data"

    def delete_all_files():
        for f in glob.glob(os.path.join(target_dir, "*")):
            if os.path.isfile(f):
                os.remove(f)

    delete_all_files()  # BEFORE the test
    yield


def test_engine_writes_and_reads():
    storage = Engine()

    puts = ["a", "z", "y", "l", "o", "0", "88", "99", "2020", "llll", "m", "zzz"]

    for p in puts:
        storage.put(p, p)

    for p in puts:
        match = storage.get(p)

        assert match is not None


def test_large_data_writes_and_reads():
    storage = Engine()

    puts = list(range(20_000))

    for p in puts:
        storage.put(p, "abc")

    for p in puts:
        match = storage.get(p)

        assert match is not None
