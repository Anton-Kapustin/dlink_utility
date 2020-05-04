from abc import ABC, abstractmethod, abstractproperty, ABCMeta


class InterfaceControllerMain(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_sys_argv(self, sys_argv):
        pass

    @abstractmethod
    def authorisation(self, ip_address):
        pass

    @abstractmethod
    def create_async_network_processes_from_ip_range(self, args, function_for_call):
        pass

    @abstractmethod
    def make_network_address(self, ip_range):
        pass

    @abstractmethod
    def make_network_gateway_address(self, ip_range):
        pass

    @abstractmethod
    def network_send_data(self, data):
        pass

    @abstractmethod
    def network_receive_data_until(self, list_read_expect):
        pass

    @abstractmethod
    def network_recieve_data(self):
        pass

    @abstractmethod
    def network_close_connection(self):
        pass

    @abstractmethod
    def get_dlink_model(self):
        pass

    @abstractmethod
    def get_current_password(self):
        pass

    @abstractmethod
    def get_model(self):
        pass


class InterfaceOperationsWithPorts(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_mac_on_port(self, ip_address, args):
        pass

    @abstractmethod
    def match_mac_from_response(self, response):
        pass

    @abstractmethod
    def get_ports_number_from_model(self, model):
        pass

    @abstractmethod
    def check_port_range(self, port_range):
        pass

