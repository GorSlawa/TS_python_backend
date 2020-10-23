import unittest


class LRUCacheTest(unittest.TestCase):
    def test_common(self):
        self.cache = LRUCache(100)
        self.cache.set('Jesse', 'Pinkman')
        self.cache.set('Walter', 'White')
        self.cache.set('Jesse', 'James')
        value = self.cache.get('Jesse')  # вернёт 'James'
        self.assertEqual(value, 'James')
        self.cache.delete('Walter')
        value = self.cache.get('Walter')  # вернёт ''
        self.assertEqual(value, '')
        self.assertEqual(self.cache.length, 1)

    def test_small_cache_01(self):
        self.cache = LRUCache(0)
        self.cache.set('Jesse', 'Pinkman')
        self.cache.set('Walter', 'White')
        value = self.cache.get('Jesse')
        self.assertEqual(value, '')
        self.assertEqual(self.cache.length, 0)

    def test_small_cache_02(self):
        self.cache = LRUCache(1)
        self.cache.set('Jesse', 'Pinkman')
        self.cache.set('Walter', 'White')
        self.cache.set('Walter', 'Black')
        value = self.cache.get('Jesse')
        self.assertEqual(value, '')
        value = self.cache.get('Walter')
        self.assertEqual(value, 'Black')
        self.assertEqual(self.cache.length, 1)


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.length = 0
        self.lru_head = None
        self.lru_tail = None
        self.lru_map = {}

    def get(self, key):
        if key not in self.lru_map:
            return ''
        else:
            node = self.lru_map[key]
            self._delete_from_list(node)
            self._add_to_head(node)
            return node.value

    def set(self, key, value):
        if key not in self.lru_map:
            if self.length == self.capacity:
                if self.capacity == 0:
                    return
                self.delete(self.lru_tail.key)
            node = Node(key, value)
            self.lru_map[key] = node
            self._add_to_head(node)
        else:
            node = self.lru_map[key]
            node.value = value
            self._delete_from_list(node)
            self._add_to_head(node)

    def delete(self, key):
        if key in self.lru_map:
            node = self.lru_map[key]
            self._delete_from_list(node)
            self.lru_map.pop(key)

    def _delete_from_list(self, node):
        if node.next is not None and node.prev is not None:
            node.prev.next, node.next.prev = node.next, node.prev
        elif node.next is not None:
            self.lru_head = node.next
            self.lru_head.prev = None
        elif node.prev is not None:
            self.lru_tail = node.prev
            self.lru_tail.next = None
        else:
            self.lru_head = None
            self.lru_tail = None
        node.next = None
        node.prev = None
        self.length -= 1

    def _add_to_head(self, node):
        assert node.next is None and node.prev is None
        if self.length == 0:
            self.lru_head = node
            self.lru_tail = node
        else:
            node.next = self.lru_head
            self.lru_head.prev = node
            self.lru_head = node
        self.length += 1
