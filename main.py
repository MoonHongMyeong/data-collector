import time
from multiprocessing import Process, Queue

from collector.cpu_collector import CpuCollector
from collector.memory_collector import MemoryCollector
from collector.storage_collector import StorageCollector
from timer.repeated_timer import RepeatedTimer
from utils.socketclient import Client
from utils.config_reader import ConfigReader

if __name__ == '__main__':

    cr = ConfigReader('collector.config')

    processes = cr.get_processes()
    IP, PORT = cr.get_ip_port()

    que = Queue()
    client = Client(que)

    client.connect(IP, PORT)

    for process in processes:
        if process['type'] == 1:
            locals()[process['name']] = CpuCollector(que)
        elif process['type'] == 2:
            locals()[process['name']] = MemoryCollector(que)
        elif process['type'] == 3:
            locals()[process['name']] = StorageCollector(que)

    set_process_idx = 1
    for process in processes:
        locals()['rt'+str(set_process_idx)] = \
            RepeatedTimer(process['interval'], locals()[process['name']].start)
        locals()['p'+str(set_process_idx)] = \
            Process(target=locals()['rt'+str(set_process_idx)].start)
        set_process_idx += 1

    set_start_process_idx = 1
    for process in processes:
        locals()['p'+str(set_start_process_idx)].start()
        set_start_process_idx += 1

    socket_process = Process(target=client.send)
    socket_process.start()

    while 1:

        time.sleep(1)

        set_start_process_idx = 1
        for process in processes:

            if not locals()['p' + str(set_start_process_idx)].is_alive():
                locals()['p' + str(set_start_process_idx)].start()

            set_start_process_idx += 1

        if not socket_process.is_alive():
            socket_process.start()
