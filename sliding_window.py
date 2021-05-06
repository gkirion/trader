from collections import deque

class SlidingWindow:

    def __init__(self, window_size):
        super().__init__()
        self.window_size = window_size
        self.window = deque()

    def add(self, item):
        if len(self.window) == self.window_size:
            self.window.popleft()
        self.window.append(item)

    def clear(self):
        self.window.clear()

    def __len__(self):
        return len(self.window)

    def __iter__(self):
        self.window_iterator = reversed(self.window)
        return self
    
    def __next__(self):
        item = next(self.window_iterator)
        return item

    def __repr__(self):
        return "window size: {window_size}, window: {window}".format(window_size = self.window_size, window = self.window)