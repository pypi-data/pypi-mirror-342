from heapq import heappush, heappop, heapify
from dataclasses import dataclass, field
from typing import Hashable


@dataclass(order=True)
class PrioritizedItem[T: Hashable]:
    priority: int
    item: T = field(compare=False)


@dataclass
class PriorityQueue[T: Hashable]:
    heap: list[PrioritizedItem[T]] = field(default_factory=list)
    lookup: dict[Hashable, PrioritizedItem[T]] = field(default_factory=dict)

    def insert(self, item: T, priority: int) -> None:
        prio_item = PrioritizedItem(priority, item)
        heappush(self.heap, prio_item)
        self.lookup[item] = prio_item

    def minimum(self) -> T:
        item = self.heap[0]
        return item.item

    def extract_min(self) -> T:
        item = heappop(self.heap)
        del self.lookup[item.item]
        return item.item

    def update_key(self, item: T, priority: int) -> None:
        prio_item = self.lookup[item]
        prio_item.priority = priority
        heapify(self.heap)
