import json
import os
import re
from datetime import datetime
from json import JSONDecodeError
from multiprocessing import Process, Queue, Event
from typing import Dict
from Model import Model
from Network import Network
from Controllers.ControllersInterface import InterfaceControllerMain


class ControllerMain(InterfaceControllerMain):

    def __init__(self, view):
        self.view = view
        self.network = Network()
        self.model = Model()

    def show_data_in_view(self, data):
        self.view.show_data(data)

    def get_model(self):
        return self.model

    def set_sys_argv(self, sys_argv):
        if self.file_settings_exists('./settings'):
            path_work_directory = self.delete_last_object_in_path(sys_argv[0])
            parameter = sys_argv[1]
            print(parameter)
            ip_range = sys_argv[2]
            args = {'parameter': parameter, 'ip_range': ip_range, 'path_work_directory': path_work_directory}
            if 'dlink_backup' in parameter:
                controller_dlink_backup = ControllerDlinkBackup(self)
                ip_dst_for_backup = sys_argv[3]
                args['ip_dst_for_backup'] = ip_dst_for_backup
                self.create_async_network_processes_from_ip_range(args, controller_dlink_backup.make_dlink_backup)
            elif 'change_password' in parameter:
                change_password = ChangePassword(self)
                login_for_new_password = sys_argv[3]
                args['login_for_new_password'] = login_for_new_password
                new_password = sys_argv[4]
                args['new_password'] = new_password
                self.create_async_network_processes_from_ip_range(args, change_password.change_password_dlink)
            elif 'mac_on_port' in parameter:
                args['ports'] = sys_argv[3]
                operations_with_ports = OperationsWithPorts(self)
                dict_ip_with_process_event_queue = self.create_async_network_processes_from_ip_range(args,
                                                                                         operations_with_ports.
                                                                                         get_mac_on_port)
                for ip in dict_ip_with_process_event_queue.keys():
                    queue: Queue = dict_ip_with_process_event_queue[ip]['queue']
                    event: Event = dict_ip_with_process_event_queue[ip]['event']
                    proc: Process = dict_ip_with_process_event_queue[ip]['process']
                    while True:
                        if event.is_set():
                            mac_on_ports = queue.get()
                            self.model.set_mac_on_ports(mac_on_ports)
                            proc.join()
                            break
                path_to_write = path_work_directory + 'mac_on_ports.txt'
                self.write_sorted_dict_to_file(path_to_write, self.model.get_mac_on_ports(), 'w+')
            else:
                print('Неверная команда')
        else:
            print('Укажите Логин и Пароль в файле settings')

    # ------------------------------------------------------------------------------------------------------------------
    #                                                 NETWORK
    # ------------------------------------------------------------------------------------------------------------------
    def authorisation(self, ip_address):
        login = self.model.get_login()
        password_list = self.model.get_password_list()
        authorised = False
        list_words_for_enter_login = [b"UserName:", b"Login", b"login:"]
        list_words_after_login = [b'#', b'>']
        response_from_connect = self.network.connect(ip_address)
        if response_from_connect:
            is_dlink_switch = self.check_switch_model(response_from_connect)
            if is_dlink_switch:
                if self.check_string_contain_item_from_list(response_from_connect, list_words_for_enter_login):
                    dlink_model = self.parse_dlink_model_name(response_from_connect)
                    if dlink_model:
                        self.model.set_dlink_model(dlink_model)
                        count_try_to_login = 0
                        while count_try_to_login < len(password_list):
                            password = password_list[count_try_to_login]
                            response_from_login = self.network.login(login, password)
                            try:
                                if self.check_string_contain_item_from_list(response_from_login,
                                                                            list_words_after_login):
                                    authorised = True
                                    self.model.set_current_password(password)
                                    break
                            except TypeError as err:
                                print(err)
                            count_try_to_login += 1
        return authorised

    # def create_async_network_processes_from_ip_range(self, args, function_for_call):
    #     ip_range = args['ip_range'].split(',')
    #     path_work_directory = args['path_work_directory']
    #     ip_addresses = self.make_network_address(ip_range)
    #     dict_ip_with_process_event_queue: Dict[str, Process] = {}
    #     if not self.write_to_log_file(path_work_directory, '', 'w'):
    #         path_work_directory = None
    #     for ip_address in ip_addresses:
    #         if ip_address:
    #             if path_work_directory:
    #                 self.write_to_log_file(path_work_directory, '', 'w')
    #             network_async_process = Process(target=function_for_call, args=(ip_address, args))
    #             network_async_process.start()
    #             dict_ip_with_process_event_queue[ip_address] = network_async_process
    #             # print(dict_ip_with_process_event_queue)
    #     while True:
    #         stop_while = False
    #         dict_copy = dict_ip_with_process_event_queue.copy()
    #         for ip in dict_ip_with_process_event_queue.keys():
    #             proc = dict_ip_with_process_event_queue[ip]
    #             # print(ip + ' alive: ' + str(proc.is_alive()))
    #             # print(self.model.get_mac_on_ports())
    #             if not proc.is_alive():
    #                 dict_copy.pop(ip)
    #             dict_copy_size = len(dict_copy)
    #             if dict_copy_size == 0:
    #                 stop_while = True
    #         if stop_while:
    #             break
    #     if 'mac_on_port' in args['parameter']:
    #         mac_on_ports_dict = self.model.get_mac_on_ports()
    #         # print(mac_on_ports_dict)
    #         # self.show_data_in_view(mac_on_ports_dict)
    #         self.write_sorted_dict_to_file('mac_on_ports.txt', mac_on_ports_dict, 'w+')
    #     return dict_copy

    def create_async_network_processes_from_ip_range(self, args, function_for_call):
        ip_range = args['ip_range'].split(',')
        path_work_directory = args['path_work_directory']
        ip_addresses = self.make_network_address(ip_range)
        dict_ip_with_process_event_queue: Dict = {}
        if not self.write_to_log_file(path_work_directory, '', 'w'):
            path_work_directory = None
        for ip_address in ip_addresses:
            queue = Queue()
            event = Event()
            if ip_address:
                if path_work_directory:
                    self.write_to_log_file(path_work_directory, '', 'w')
                args['queue'] = queue
                args['event'] = event
                network_async_process = Process(target=function_for_call, args=(ip_address, args))
                network_async_process.start()
                dict_ip_with_process_event_queue[ip_address] = {'process': network_async_process,
                                                                 'queue': queue, 'event': event}
        return dict_ip_with_process_event_queue

    def make_network_address(self, ip_range):
        list_ip_addresses = []
        start_ip_range = ip_range[0]
        end_ip_range = ip_range[1]
        start_ip_range_splited = start_ip_range.split('.')
        end_ip_range_splited = end_ip_range.split('.')
        third_octet_in_start_ip_range = int(start_ip_range_splited[2])
        third_octet_in_end_ip_range = int(end_ip_range_splited[2])
        last_octet_in_start_ip_range = int(start_ip_range_splited[3])
        last_octet_in_end_ip_range = int(end_ip_range_splited[3])
        if self.check_ip_range_correct(third_octet_in_start_ip_range, third_octet_in_end_ip_range,
                                       last_octet_in_start_ip_range, last_octet_in_end_ip_range):
            if third_octet_in_start_ip_range == third_octet_in_end_ip_range:
                network = str(start_ip_range_splited[0]) + '.' + str(start_ip_range_splited[1]) + '.' + \
                          str(third_octet_in_start_ip_range)
                if last_octet_in_start_ip_range == 0:
                    last_octet_in_start_ip_range = 1
                for last_octet_ip in range(last_octet_in_start_ip_range, last_octet_in_end_ip_range + 1):
                    ip_address = network + '.' + str(last_octet_ip)
                    list_ip_addresses.append(ip_address)
            elif third_octet_in_start_ip_range < third_octet_in_end_ip_range:
                for third_octet in range(third_octet_in_start_ip_range, third_octet_in_end_ip_range + 1):
                    if third_octet < third_octet_in_end_ip_range:
                        last_octet_in_end_of_range = 254
                    else:
                        last_octet_in_end_of_range = last_octet_in_end_ip_range
                    for last_octet in range(last_octet_in_start_ip_range, last_octet_in_end_of_range + 1):
                        network = str(start_ip_range_splited[0]) + '.' + str(start_ip_range_splited[1]) + '.'
                        if last_octet > 0:
                            ip_address = network + str(third_octet) + '.' + str(last_octet)
                            list_ip_addresses.append(ip_address)
        else:
            list_ip_addresses = None
        return list_ip_addresses

    def make_network_gateway_address(self, ip_range):
        ip_addresses_list = self.make_network_address(ip_range)
        first_ip_address_in_list = ip_addresses_list[0]
        first_ip_address_in_list_splited = first_ip_address_in_list.split('.')
        third_octet_in_ip = int(first_ip_address_in_list_splited[2]) + 1
        first_ip_address_in_list_splited[2] = str(third_octet_in_ip)
        first_ip_address_in_list_splited[-1] = '254'
        gateway_address = ""
        for octet in first_ip_address_in_list_splited:
            gateway_address += octet + '.'
        gateway = gateway_address[:-1]
        return gateway

    def network_send_data(self, data):
        result = self.network.send_data(data)
        return result

    def network_receive_data_until(self, list_read_expect):
        response = self.network.receive_data_until(list_read_expect)
        return response

    def network_recieve_data(self):
        return self.network.recieve_data()

    def network_close_connection(self):
        self.network.close_conection()

    def get_dlink_model(self):
        return self.model.get_dlink_model()

    def get_current_password(self):
        return self.model.get_current_password()

    @staticmethod
    def check_ip_range_correct(third_octet_in_start_range, third_octet_in_end_ip_range,
                               last_octet_in_start_ip_range, last_octet_in_end_ip_range):
        if third_octet_in_start_range <= third_octet_in_end_ip_range and \
                last_octet_in_start_ip_range <= last_octet_in_end_ip_range:
            return True
        else:
            return False

    @staticmethod
    def parse_dlink_model_name(raw_response_with_model_name):
        dlink_model = ''
        try:
            dlink_model_name = re.sub(r'[*\t\r\n>]', '', raw_response_with_model_name.decode('UTF-8'))
            # print(dlink_model_name)
            dlink_model_name = re.findall(r'D[GE]S-\d+-\d+\w+/ME|D[GE]S-\d+-\d+\w{1,2}(?=[\s\D])', dlink_model_name)
            if ':' in dlink_model_name:
                model = dlink_model_name[0].split(':')
                dlink_model = model[0]
            else:
                dlink_model = dlink_model_name[0]
        except IndexError as err:
            print(err)
        return dlink_model

    @staticmethod
    def check_switch_model(checking_string):
        hp_models_list = ['ProCurve', ' HP ', 'Hewlett']
        dlink_models_list = ['D-link', 'd-link', 'DGS', 'DES']
        checking_string_decoded = checking_string.decode('utf-8')
        is_dlink_model = False
        for hp_model in hp_models_list:
            for dlink_model in dlink_models_list:
                if hp_model in checking_string_decoded:
                    is_dlink_model = False
                elif dlink_model in checking_string_decoded:
                    is_dlink_model = True
        return is_dlink_model

    @staticmethod
    def is_web_smart_model(dlink_model):
        if dlink_model:
            if '1210' in dlink_model and 'ME' not in dlink_model:
                result = True
            else:
                result = False
        else:
            result = False
        return result

    @staticmethod
    def check_string_contain_item_from_list(string_for_check, list_with_checking_words):
        result = None
        if string_for_check is not None:
            for word in list_with_checking_words:
                if word in string_for_check:
                    result = word.decode('utf-8')
            return result

    @staticmethod
    def get_date_in_string():
        date_now = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        return date_now

    @staticmethod
    def delete_last_object_in_path(path_argv):
        path = re.sub(r'(\w+\.py$)|(\w+[\w\-]\w+/$)', '', path_argv)
        # print(path)
        return path

    @staticmethod
    def write_to_log_file(path, string_to_write, write_parameter):
        path += 'Log'
        # print(path)
        try:
            os.stat(path)
        except OSError as err:
            print(err)
            os.mkdir(path)
        try:
            log_file_path = path + '/log.txt'
            file_log = open(log_file_path, write_parameter)
            file_log.write(string_to_write + '\n')
            file_log.close()
            result = True
        except OSError as err:
            print(err)
            result = False
        return result

    def write_data_to_file(self, path, data, write_parameter):
        # print(path)
        try:
            os.stat(path)
        except OSError as err:
            print(err)
        try:
            file = open(path, write_parameter)
            file.write(data + '\n')
            file.close()
            result = True
        except OSError as err:
            print(err)
            result = False
        return result

    @staticmethod
    def write_sorted_dict_to_file(path, dict_to_write: dict, write_parameter):
        try:
            os.stat(path)
        except OSError as err:
            print(err)
        try:
            file = open(path, write_parameter)
            i = 0
            for ip in sorted(dict_to_write.keys()):
                if i > 0:
                    file.write('\n')
                file.write(ip + '\n')
                i += 1
                j = 0
                for port, mac_list in dict_to_write[ip].items():
                    file.write(str(port) + ' port:\n')
                    for mac in mac_list:
                        file.write(mac + '\n')
            file.close()
            result = True
        except OSError as err:
            print(err)
            result = False
        return result

    @staticmethod
    def check_folder_exists(path_folder):
        try:
            os.stat(path_folder)
        except OSError as err:
            print(err)
            print('create folder: ' + path_folder)
            os.mkdir(path_folder)

    def file_settings_exists(self, path_file):
        file_settings_exists = False
        txt_login: str = 'login'
        txt_password = 'password'
        txt_enter_login = 'Добавьте логин и пароль в файл settings (pass1 и pass2 заменить на актуальные пароли)'
        params_to_write = '{"login": "", "password": ["pass1", "pass2"]}'
        settings = {}
        try:
            try:
                os.stat(path_file)
            except OSError as err:
                print(err)
                file = open(path_file, 'w+')
                file.close()
            file_settings = open(path_file, mode='r+')
            try:
                settings = json.load(file_settings)
            except JSONDecodeError as err:
                print(err)
                print(txt_enter_login)
                try:
                    file_settings.write(params_to_write)
                except AttributeError as err:
                    print('attr error' + str(err))
            # print(settings)
            if settings:
                if 'login' in settings and 'password' in settings:
                    login = settings[txt_login]
                    file_settings_exists = True
                    if len(login) != 0:
                        self.model.set_login(settings[txt_login])
                        self.model.set_password_list(settings[txt_password])
                    else:
                        print(txt_enter_login)
                        file_settings_exists = False
                else:
                    file_settings.write(params_to_write)
                    print(txt_enter_login)
            file_settings.close()
        except IOError as err:
            print('check_file_exists: ' + str(err))
        except AttributeError as err:
            print(err)
        return file_settings_exists


from Controllers.OperationsWithPorts import OperationsWithPorts
from Controllers.ChangePassword import ChangePassword
from Controllers.ControllerDlinkBackup import ControllerDlinkBackup