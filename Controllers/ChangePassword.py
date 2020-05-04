from Controllers import ControllerMain


class ChangePassword:

    def __init__(self, controller_main: ControllerMain):
        self.controller = controller_main

    def change_password_dlink(self, ip_address, args):
        login_for_new_password = args['login_for_new_password']
        new_passwod = args['new_password']
        print(args)
        if self.controller.authorisation(ip_address):
            print('authorized')
            model = self.controller.get_dlink_model()
            print(model)
            if model:
                if self.check_login_exist_on_switch(login_for_new_password):
                    current_password = self.controller.get_current_password()
                    cmd = 'config account ' + login_for_new_password + '\n'
                    self.controller.network_send_data(cmd)
                    print(cmd)
                    data = self.controller.network_receive_data_until([b'Enter an old password:'])
                    if data:
                        self.controller.network_send_data(current_password + '\n')
                        self.controller.network_send_data(new_passwod + '\n')
                        self.controller.network_send_data(new_passwod + '\n')
                        data = self.controller.network_receive_data_until([b'Success', b'Password do not match.'])
                        print(data)
                        if 'Success' in data.decode('utf-8'):
                            return True

    def check_login_exist_on_switch(self, login_for_check):
        cmd = 'show account\n'
        self.controller.network_send_data(cmd)
        data = self.controller.network_receive_data_until([b'Total'])
        print(login_for_check)
        print(data)
        if data:
            if login_for_check in data.decode('utf-8'):
                return True
            else:
                return False
