from telnetlib import Telnet
import re


class Network:

    def __init__(self):
        self.LOG_TAG = self.__class__.__name__ + ": "
        self.telnet_connection = Telnet()

    def connect(self, ip):
        read_until_word = [b"\r\n\r\nUserName: ", b"Login", b"login:"]
        response = None
        if self.check_ip(ip):
            try:
                self.telnet_connection.open(ip, timeout=5)
                i, obj, response = self.telnet_connection.expect(read_until_word, 3)
                return response
            except IOError as err:
                print(self.LOG_TAG + ip + ' ' + str(err))
                return response
            except EOFError as err:
                print(self.LOG_TAG + ip + ' ' + str(err))
                return response
        else:
            return response

    def login(self, login, password=''):
        read_until_password = [b'ord:']
        response = None
        if login:
            try:
                self.telnet_connection.write(login.encode() + b'\r\n')
                i, obj, response = self.telnet_connection.expect(read_until_password, 3)
                if 'ord' in response.decode('utf-8'):
                    self.telnet_connection.write(password.encode() + b'\r\n')
                    i, obj, response = self.telnet_connection.expect([b'\#|\>'], 6)
                    return response
            except IOError as err:
                print(self.LOG_TAG + str(err))
                return response
            except EOFError as err:
                print(self.LOG_TAG + str(err))
                return response
        else:
            return response

    def recieve_data(self):
        data = None
        try:
            raw_data = self.telnet_connection.read_very_eager()
            data = raw_data.decode('utf-8')
            return data
        except IOError as err:
            print(self.LOG_TAG + str(err))
            return data
        except EOFError as err:
            print(self.LOG_TAG + str(err))
            return data

    def receive_data_until(self, list_expect):
        response = None
        try:
            i, obj, response = self.telnet_connection.expect(list_expect, 25)
        except IOError as err:
            print(self.LOG_TAG + str(err))
        except EOFError as err:
            print(self.LOG_TAG + str(err))
        return response

    def send_data(self, data):
        sending_result = False
        # print(data)
        # print(data.encode('utf-8'))
        try:
            self.telnet_connection.write(data.encode())
            sending_result = True
        except IOError as err:
            print(self.LOG_TAG + str(err))
        except EOFError as err:
            print(self.LOG_TAG + str(err))
        return sending_result

    def close_conection(self):
        closing_connection_result = False
        try:
            self.telnet_connection.close()
            closing_connection_result = True
        except IOError as err:
            print(self.LOG_TAG + str(err))
        except EOFError as err:
            print(self.LOG_TAG + str(err))
        return closing_connection_result

    @staticmethod
    def check_ip(ip):
        if not ip:
            return False
        else:
            regex = re.findall(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
            if regex:
                return True
            else:
                return False

    def check_switch_model(self, checking_string):
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


