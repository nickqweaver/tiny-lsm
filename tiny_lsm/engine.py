from pathlib import Path

from tiny_lsm.memtable import MemTable


# Before compaction maybe we will handle reads
class Engine:
    _ss_table_level = 0

    def __init__(self):
        self.__memtable = MemTable(2)
        self._init_table_level()

    def _init_table_level(self):
        data_folder = Path("data")
        all_files = [f for f in data_folder.iterdir() if f.is_file()]

        level = len(all_files)
        self._ss_table_level = level

        return level

    def _traverse_tables(self, key):

        matched_key_value = None
        for level in range(self._ss_table_level, 0, -1):
            if matched_key_value is not None:
                return matched_key_value

            with open(f"data/{level}_sstable.txt", "r") as ss_table:
                # Ideally we would binary search the sstable, but for simplicity we scan the full file
                for line in ss_table:
                    k, value = line.split("\t")
                    if k == key:
                        matched_key_value = value

        return matched_key_value

    def put(self, key, value):
        # If full before adding we will flush then add
        print(f"Adding store size is {self.__memtable.size}")
        if self.__memtable.size >= self.__memtable.capacity:
            self.flush()

        return self.__memtable.set(key, value)

    def get(self, key):
        hit = self.__memtable.get(key)

        if hit:
            print("cache hit", key)
            return hit

        # Look at the SS tables
        return self._traverse_tables(key)

    def flush(self):
        in_memory = self.__memtable.empty()

        level = self._ss_table_level
        next_level = level + 1
        self._ss_table_level = next_level
        filename = f"{next_level}_sstable.txt"

        with open(f"data/{filename}", "a+") as file:
            for k, v in in_memory:
                file.write(f"{k}\t{v}\n")
