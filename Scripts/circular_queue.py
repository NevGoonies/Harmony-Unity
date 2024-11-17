# keeps the last n items

class CircularQueue:
    def __init__(self, n):
        self.n = n
        self.data = []
        self.index = 0

    def append(self, item):
        self.data.append(item)
        if len(self.data) > self.n:
            self.data.pop(0)
        self.index += 1