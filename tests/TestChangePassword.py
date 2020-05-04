import unittest
from unittest.mock import patch

from Controllers.ChangePassword import ChangePassword
from Controllers.ControllerMain import ControllerMain


class TestChangePassword(unittest.TestCase):

    def setUp(self) -> None:
        self.controllerMain = ControllerMain('')
        self.changePassword = ChangePassword(self.controllerMain)

    @patch('ChangePassword.ChangePassword.check_login_exist_on_switch')
    @patch('sys.exit')
    @patch('ControllerMain.ControllerMain.get_current_password')
    @patch('ControllerMain.ControllerMain.get_dlink_model')
    @patch('ControllerMain.ControllerMain.network_close_connection')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    def test_dlink_change_password(self, mock_receive_data_until, mock_send_data, mock_authorisation,
                                   mock_close_connection, mock_get_dlink_model, mock_get_current_password,
                                   mock_sys_exit, mock_check_login_exist_on_switch):
        mock_authorisation.return_value = True
        mock_receive_data_until.return_value = b'Success'
        mock_send_data.return_value = True
        mock_close_connection.return_value = True
        mock_sys_exit.return_value = True
        mock_check_login_exist_on_switch.return_value = True
        mock_get_dlink_model.return_value = 'DGS-1210-10P/ME'
        mock_get_current_password.return_value = '213'
        ip_address = '172.1.2.50'
        args = {'login_for_new_password': 'admin', 'new_password': '1234'}
        return_result = self.changePassword.change_password_dlink(ip_address, args)
        self.assertTrue(return_result)

    @patch('ChangePassword.ChangePassword.check_login_exist_on_switch')
    @patch('sys.exit')
    @patch('ControllerMain.ControllerMain.get_current_password')
    @patch('ControllerMain.ControllerMain.get_dlink_model')
    @patch('ControllerMain.ControllerMain.network_close_connection')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    def test_dlink_change_password_authorisation_unsuccess(self, mock_receive_data_until, mock_send_data, mock_authorisation,
                                   mock_close_connection, mock_get_dlink_model, mock_get_current_password,
                                   mock_sys_exit, mock_check_login_exist_on_switch):
        mock_authorisation.return_value = False
        mock_receive_data_until.return_value = b'Success'
        mock_send_data.return_value = True
        mock_close_connection.return_value = True
        mock_sys_exit.return_value = True
        mock_check_login_exist_on_switch.return_value = True
        mock_get_dlink_model.return_value = 'DGS-1210-10P/ME'
        mock_get_current_password.return_value = '213'
        ip_address = '172.1.2.50'
        args = {'login_for_new_password': 'admin', 'new_password': '1234'}
        return_result = self.changePassword.change_password_dlink(ip_address, args)
        self.assertFalse(return_result)

    @patch('ChangePassword.ChangePassword.check_login_exist_on_switch')
    @patch('sys.exit')
    @patch('ControllerMain.ControllerMain.get_current_password')
    @patch('ControllerMain.ControllerMain.get_dlink_model')
    @patch('ControllerMain.ControllerMain.network_close_connection')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    def test_dlink_change_password_login_exist_unsuccess(self, mock_receive_data_until, mock_send_data, mock_authorisation,
                                   mock_close_connection, mock_get_dlink_model, mock_get_current_password,
                                   mock_sys_exit, mock_check_login_exist_on_switch):
        mock_authorisation.return_value = True
        mock_receive_data_until.return_value = b'Success'
        mock_send_data.return_value = True
        mock_close_connection.return_value = True
        mock_sys_exit.return_value = True
        mock_check_login_exist_on_switch.return_value = False
        mock_get_dlink_model.return_value = 'DGS-1210-10P/ME'
        mock_get_current_password.return_value = '213'
        ip_address = '172.1.2.50'
        args = {'login_for_new_password': 'admin', 'new_password': '1234'}
        return_result = self.changePassword.change_password_dlink(ip_address, args)
        self.assertFalse(return_result)

    @patch('ChangePassword.ChangePassword.check_login_exist_on_switch')
    @patch('sys.exit')
    @patch('ControllerMain.ControllerMain.get_current_password')
    @patch('ControllerMain.ControllerMain.get_dlink_model')
    @patch('ControllerMain.ControllerMain.network_close_connection')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    def test_dlink_change_password_receive_data_unsuccess(self, mock_receive_data_until, mock_send_data,
                                                         mock_authorisation,
                                                         mock_close_connection, mock_get_dlink_model,
                                                         mock_get_current_password,
                                                         mock_sys_exit, mock_check_login_exist_on_switch):
        mock_authorisation.return_value = True
        mock_receive_data_until.return_value = b''
        mock_send_data.return_value = True
        mock_close_connection.return_value = True
        mock_sys_exit.return_value = True
        mock_check_login_exist_on_switch.return_value = True
        mock_get_dlink_model.return_value = 'DGS-1210-10P/ME'
        mock_get_current_password.return_value = '213'
        ip_address = '172.1.2.50'
        args = {'login_for_new_password': 'admin', 'new_password': '1234'}
        return_result = self.changePassword.change_password_dlink(ip_address, args)
        self.assertFalse(return_result)

    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    @patch('ControllerMain.ControllerMain.network_send_data')
    def test_change_password_check_login_exist_on_switch_success(self, mock_network_send_data,
                                                                              mock_network_receive_data_until):
        mock_network_send_data.return_value = True
        mock_network_receive_data_until.return_value = b'admin'
        login_for_check = 'admin'
        self.assertTrue(self.changePassword.check_login_exist_on_switch(login_for_check))

    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    @patch('ControllerMain.ControllerMain.network_send_data')
    def test_change_password_check_login_exist_on_switch_unsuccess(self, mock_network_send_data,
                                                                              mock_network_receive_data_until):
        mock_network_send_data.return_value = True
        mock_network_receive_data_until.return_value = b'no'
        login_for_check = 'admin'
        self.assertFalse(self.changePassword.check_login_exist_on_switch(login_for_check))