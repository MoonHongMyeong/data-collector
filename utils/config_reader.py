class ConfigReader:

    def __init__(self, path):
        file = open(path, 'r')
        lines = file.readlines()
        file.close()
        lines = ''.join(lines)
        lines = lines.replace('  ', '')
        lines = lines.split('\n')

        socket_info = []
        name = []
        collector_type = []
        interval = []
        process_info = []

        for line in lines:
            if 'type: ' in line:
                collector_type.append(line.replace('type: ', ''))
            elif 'name: ' in line:
                name.append(line.replace('name: ', ''))
            elif 'interval: ' in line:
                interval.append(int(line.replace('interval: ', '')))
            elif 'ip: ' in line:
                socket_info.append(line.replace('ip: ', ''))
            elif 'port: ' in line:
                socket_info.append(int(line.replace('port: ', '')))

        for i in range(0, len(name)):
            dict_process = {'type': collector_type[i], 'name': name[i], 'interval': interval[i]}
            process_info.append(dict_process)

        self._process = process_info
        self._socket = socket_info

    def get_processes(self):
        return self._process

    def get_ip_port(self):
        return self._socket
