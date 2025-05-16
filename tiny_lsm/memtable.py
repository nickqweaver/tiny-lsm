class MemTable:
    def __init__(self, capacity):
        self.__store = {}
        # Capacity would typically be measured in bytes but we're going to measure number of k/v pairs
        self.capacity = capacity

    def _to_list(self):
        def sort_by_key(value):
            key = value[0]
            return key

        items = self.__store.items()

        items_list = list(items)
        items_list.sort(key=sort_by_key)

        return items_list

    @property
    def size(self):
        return len(self.__store)

    def set(self, key, value):
        self.__store[key] = value

    def get(self, key):
        return self.__store.get(key)

    def is_full(self):
        return self.size > self.capacity

    def empty(self):
        payload = self._to_list()
        self.__store = {}

        return payload
