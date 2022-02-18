import struct
import time
import psutil

from collector.collector import Collector


class CpuCollector(Collector):

    def __init__(self, queue):
        self.type = 1
        self._format = '@hfd'
        self._is_running = False
        self._queue = queue

    def _collect_data(self):
        rate = psutil.cpu_percent()
        timestamp = time.time()

        return rate, timestamp

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
        super(CpuCollector, self).start()

    def stop(self):
        super(CpuCollector, self).stop()
