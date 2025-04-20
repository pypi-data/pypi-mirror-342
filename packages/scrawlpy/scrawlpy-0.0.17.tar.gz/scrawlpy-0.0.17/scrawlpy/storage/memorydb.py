# -*- coding: utf-8 -*-
# @Time   : 2024/4/30 18:01
import queue


class MemoryDB:
    def __init__(self):
        self._storage = {}
        self.priority_queue = queue.PriorityQueue(maxsize=0)

    def set(self, key, value):
        self._storage[key] = value

    def add(self, item, priority: int = 0, ignore_max_size=False) -> None:
        """
        添加数据到优先级队列中
        Args:
            item: 数据
            priority: 优先级，数字越小优先级越高
            ignore_max_size: queue满时是否等待，为True时无视队列的maxsize，直接往里塞

        Returns:

        """
        self.priority_queue.put((priority, item))

    def get(self) -> str:
        """
        从优先级队列中获取种子URL，数字越小优先级越高
        Returns:

        """
        return self.priority_queue.get()

    def get_nowait(self):
        """
        从优先级队列中获取种子URL，数字越小优先级越高
        Returns:

        """
        try:
            return self.priority_queue.get_nowait()
        except queue.Empty:
            return None

    def size(self):
        return self.priority_queue.qsize()

    def get_all(self):
        return self.priority_queue.empty()

    def is_empty(self):
        return self.priority_queue.empty()

    def clear(self):
        self.priority_queue.queue.clear()

    def delete(self, key):
        if key in self._storage:
            del self._storage[key]


if __name__ == '__main__':
    db = MemoryDB()
    db.add("https://www.baidu.com", priority=3)
    db.add("https://www.baidu.com", 14)
    db.add("https://www.baidu.com", 2)
    # print(db.get())
    print(db.size())
    print(db.clear())
    print(db.size())
    print(db.get_nowait())
