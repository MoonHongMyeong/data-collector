import struct
import time

import psutil

from collector.collector import Collector


class StorageCollector(Collector):

    def __init__(self, queue, pipe):
        self.type = 3
        self._format = '@hfd'
        self._queue = queue
        self._pipe = pipe

    def _collect_data(self):
        disk_rate = psutil.disk_usage("/").percent
        timestamp = time.time()
        return disk_rate, timestamp

    def _send_socket(self, data):
        self._queue.put(data)

    def _format_struct_to_data(self, data):
        return struct.pack(self._format, self.type, data[0], data[1])

    def _run(self):
        collected_data = self._collect_data()
        pack_data = self._format_struct_to_data(collected_data)
        self._send_socket(pack_data)

    def start(self):
        while 1:
            if self._pipe.recv() is not None:
                self._run()
