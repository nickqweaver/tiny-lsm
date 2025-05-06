from tiny_lsm.memtable import MemTable


# need to dump to new sstable when capacity is hit
class Engine:

    def __init__(self):
        self.__memtable = MemTable(8)

    def put(self, key, value):
        return self.__memtable.set(key, value)

    def get(self, key):
        return self.__memtable.get(key)

    def flush(self):
        # Write to the file
        in_memory = self.__memtable.flush()

        with open("ss_table.txt", "w") as file:
            for k, v in in_memory:
                file.write(f"{k}, {v} \n")
