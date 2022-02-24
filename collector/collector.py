from abc import *


class Collector(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        self._is_running = False

    @abstractmethod
    def _collect_data(self):
        pass

    @abstractmethod
    def _send_socket(self, data):
        pass

    @abstractmethod
    def _run(self):
        pass

    @abstractmethod
    def start(self):
        pass
