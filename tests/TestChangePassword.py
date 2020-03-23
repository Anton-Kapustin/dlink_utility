import unittest
from unittest.mock import patch

from ChangePassword import ChangePassword
from ControllerMain import ControllerMain


class TestChangePassword(unittest.TestCase):

    def setUp(self) -> None:
        self.controllerMain = ControllerMain('')
        self.changePassword = ChangePassword('')

    @patch('sys.exit')
    @patch('ControllerMain.ControllerMain.network_close_connection')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    def test_dlink_change_password(self, mock_receive_data_until, mock_send_data, mock_authorisation,
                                   mock_close_connection, mock_sys_exit):
        mock_authorisation.return_value = True
        mock_receive_data_until.return_value = 'Success'
        mock_send_data.return_value = True
        mock_close_connection.return_value = True
        mock_sys_exit.return_value = True
        cmd = 'cmd'
        ip_addrass = '172.1.2.86'
        model = 'DGS-1210-10P/ME'
        login_for_new_password = 'admin'
        new_password = '1234'
        return_result = self.changePassword.change_password_dlink(login_for_new_password, new_password)
        self.assertTrue(return_result)
