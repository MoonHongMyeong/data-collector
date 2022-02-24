import time


class CustomTimer:

    def __init__(self, processes):
        self._processes = processes
        self._count = 0
        self._next_call = time.time()

    def start(self):
        while 1:
            self._count += 1
            self._next_call += 1
            for process in self._processes:
                if self._count % (process[1] / 1000) == 0:
                    if process[0] == 1:
                        process[2].send(0)
                    elif process[0] == 2:
                        process[2].send(0)
                    elif process[0] == 3:
                        process[2].send(0)
            time.sleep(self._next_call - time.time())
