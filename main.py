import time
from multiprocessing import Process, Queue, Pipe

from collector.cpu_collector import CpuCollector
from collector.memory_collector import MemoryCollector
from collector.storage_collector import StorageCollector
from timer.custom_timer import CustomTimer
from utils.socketclient import Client
from utils.config_reader import ConfigReader

if __name__ == '__main__':

    cr = ConfigReader('collector.config')

    processes = cr.get_processes()
    IP, PORT = cr.get_ip_port()

    que = Queue()

    client = Client(que)
    client.connect(IP, PORT)

    pipes = []
    index = 1

    for process in processes:
        locals()['p_con' + str(index)], locals()['c_con' + str(index)] = Pipe()
        pipes.append((process['type'], process['interval'], locals()['p_con' + str(index)]))

        locals()[process['name']] = locals()[process['type']](que, locals()['c_con' + str(index)])

        locals()['p' + str(index)] = Process(target=locals()[process['name']].start)
        locals()['p' + str(index)].start()

        index += 1

    socket_process = Process(target=client.send)
    socket_process.start()

    timer = CustomTimer(pipes)
    timer_process = Process(target=timer.start)
    timer_process.start()

    while 1:

        time.sleep(1)

        start_process_idx = 1
        for process in processes:

            if not locals()['p' + str(start_process_idx)].is_alive():
                locals()['p' + str(start_process_idx)].kill()
                locals()['p' + str(start_process_idx)].start()

            start_process_idx += 1

        if not socket_process.is_alive():
            socket_process.kill()
            socket_process.start()
