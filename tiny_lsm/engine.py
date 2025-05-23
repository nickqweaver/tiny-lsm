import os
from pathlib import Path

from tiny_lsm.memtable import MemTable


class Engine:
    _ss_table_level = 0

    def __init__(self):
        self.__memtable = MemTable(500)
        self._init_table_level()

    def _init_table_level(self):
        data_folder = Path("data")
        all_files = [f for f in data_folder.iterdir() if f.is_file()]

        level = len(all_files)
        self._ss_table_level = level

        return level

    def _compact(self):
        store = {}

        for level in range(self._ss_table_level, 0, -1):
            file = f"data/{level}_sstable.txt"
            with open(file, "r") as ss_table:
                for line in ss_table:
                    key, value = line.split("\t")

                    if key not in store:
                        store[key] = value
            os.remove(file)

        def sort_by_key(value):
            key = value[0]
            return key

        items = store.items()

        items_list = list(items)
        items_list.sort(key=sort_by_key)

        self._ss_table_level = 1
        filename = "1_sstable.txt"

        with open(f"data/{filename}", "a+") as file:
            for k, v in items_list:
                file.write(f"{k}\t{v}")

    def _traverse_tables(self, key):
        matched_key_value = None
        for level in range(self._ss_table_level, 0, -1):
            if matched_key_value is not None:
                return matched_key_value

            with open(f"data/{level}_sstable.txt", "r") as ss_table:
                # Ideally we would binary search the sstable, but for simplicity we scan the full table
                for line in ss_table:
                    k, value = line.split("\t")
                    if k == key:
                        matched_key_value = value

        return matched_key_value

    def put(self, key, value):
        k = str(key)

        self.__memtable.set(k, value)

        if self.__memtable.size >= self.__memtable.capacity:
            self.flush()

        if self._ss_table_level >= 25:
            self._compact()

    def get(self, key):
        hit = self.__memtable.get(key)

        k = str(key)
        if hit:
            return hit

        # Look at the SS tables
        return self._traverse_tables(k)

    def flush(self):
        in_memory = self.__memtable.empty()

        level = self._ss_table_level
        next_level = level + 1
        self._ss_table_level = next_level
        filename = f"{next_level}_sstable.txt"

        with open(f"data/{filename}", "a+") as file:
            for k, v in in_memory:
                file.write(f"{k}\t{v}\n")
