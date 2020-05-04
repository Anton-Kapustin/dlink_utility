class Model:

    def __init__(self):
        self.login = ''
        self.__password_list = []
        self.password_model_me = ''
        self.password_root = ''
        self.password_model_websmart = ''
        self.dlink_model = ''
        self.current_password = ''
        self.mac_on_ports: dict = {}

    def set_mac_on_ports(self, mac_on_ports):
        if mac_on_ports:
            self.mac_on_ports.update(mac_on_ports)

    def get_mac_on_ports(self):
        return self.mac_on_ports

    def set_current_password(self, current_password):
        self.current_password = current_password

    def get_current_password(self):
        return self.current_password

    def set_login(self, login):
        self.login = login

    def get_login(self):
        return self.login

    def get_password_list(self):
        return self.__password_list

    def set_password_list(self, passwords):
        self.__password_list = passwords

    def get_password_root(self):
        return self.password_root

    def set_password_model_me(self, password):
        self.password_model_me = password

    def get_password_model_me(self):
        return self.password_model_me

    def set_password_model_websmart(self, password):
        self.password_model_websmart = password

    def get_password_model_websmart(self):
        return self.password_model_websmart

    def set_dlink_model(self, model_name):
        self.dlink_model = model_name

    def get_dlink_model(self):
        return self.dlink_model
