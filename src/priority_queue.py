
from typing import List, Tuple, Any

class PriorityQueue:
    queue: List[tuple] = []

    def empty(self) -> bool:
        return len(self.queue) == 0


    def put(self, element: Tuple[int, Any]):
        self.queue.append(element)


    def get(self) -> tuple:
        if self.empty():
            raise IndexError('No elements in the list')
        
        min = 0
        for index in range(len(self.queue)):
            if self.queue[index][0] < self.queue[min][0]:
                min = index

        return self.queue.pop(min)
