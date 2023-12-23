import time

class Fps():
    prev_time = 1
    fps = 1

    def __init__(self):
        self.prev_time = time.time()
        time.sleep(0.1)

    def calc(self):
        self.fps = int(1 / (time.time() - self.prev_time))
        self.prev_time = time.time()
        return self.fps