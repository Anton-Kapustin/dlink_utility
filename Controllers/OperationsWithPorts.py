import re
from multiprocessing import Event
from multiprocessing.queues import Queue

from Controllers.ControllerMain import ControllerMain
from Controllers.ControllersInterface import InterfaceOperationsWithPorts


class OperationsWithPorts(InterfaceOperationsWithPorts):

    def __init__(self, controller: ControllerMain):
        self.controller = controller

    def check_port_range(self, ports):
        ports_range = []
        if ports:
            ports_range_splited = ports.split('-')
            try:
                ports_range = [int(port) for port in ports_range_splited]
                for i, port in enumerate(ports_range):
                    if port == 0:
                        ports_range[i] = 1
                if len(ports_range) == 1:
                    ports_range.append(ports_range[0] + 1)
            except ValueError as err:
                ports_range = None
        return ports_range

    def get_mac_on_port(self, ip_address, args):
        mac_on_port = {ip_address: {}}
        queue: Queue = args['queue']
        event: Event = args['event']
        if ip_address:
            ports_range = self.check_port_range(args['ports'])
            if ports_range:
                first_port = ports_range[0]
                last_port = ports_range[1]
                if self.controller.authorisation(ip_address):
                    dlink_model = self.controller.get_dlink_model()
                    if not self.controller.is_web_smart_model(dlink_model):
                        dlink_ports = self.get_ports_number_from_model(dlink_model)
                        if last_port > dlink_ports:
                            last_port = dlink_ports
                        for port in range(first_port, last_port + 1):
                            cmd = 'show fdb port ' + str(port) + '\n'
                            self.controller.network_send_data(cmd)
                            list_read_until = [b'Next', b'NEXT', b'#']
                            data = self.controller.network_receive_data_until(list_read_until)
                            if data:
                                if self.controller.check_string_contain_item_from_list(data, list_read_until):
                                    self.controller.network_send_data('q\n')
                                mac_list = self.match_mac_from_response(data)
                                if mac_list:
                                    mac_on_port[ip_address][port] = mac_list
                                    print(mac_on_port)
                    else:
                        mac_on_port[ip_address][0] = ['websmart']
            else:
                print('Неверный список портов')
        queue.put(mac_on_port)
        event.set()
        return mac_on_port

    def match_mac_from_response(self, response):
        mac_list = []
        if response:
            regex = r"[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}"
            mac_list = re.findall(regex, response.decode('utf-8'))
        return mac_list

    def get_ports_number_from_model(self, model):
        model_splited = model.split('-')
        ports = re.findall(r'^\d+', model_splited[2])
        if ports:
            ports = int(ports[0])
        return ports
