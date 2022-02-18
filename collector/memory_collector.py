import struct
import time

import psutil

from collector.collector import Collector


class MemoryCollector(Collector):

    def __init__(self, queue):
        self.type = 2
        self._format = '@hfd'
        self._is_running = False
        self.memory = psutil.virtual_memory()
        self._queue = queue

    def _collect_data(self):
        memory_rate = self.memory.percent
        timestamp = time.time()

        return memory_rate, timestamp

    def _send_socket(self, data):
        self._queue.put(data)

    def _format_struct_to_data(self, data):
        return struct.pack(self._format, self.type, data[0], data[1])

    def _run(self):
        collected_data = self._collect_data()
        pack_data = self._format_struct_to_data(collected_data)

        self._send_socket(pack_data)

        self.stop()

    def start(self):
        super(MemoryCollector, self).start()
        
    def stop(self):
        super(MemoryCollector, self).stop()
