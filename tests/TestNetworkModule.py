import unittest
from unittest.mock import patch

from Network import Network


class TestNetworkModule(unittest.TestCase):

    def setUp(self):
        self.network = Network()

    @patch('telnetlib.Telnet.close')
    @patch('telnetlib.Telnet.read_very_eager')
    @patch('telnetlib.Telnet.write')
    @patch('telnetlib.Telnet.expect')
    @patch('telnetlib.Telnet.open')
    def test_connect_reponse_not_empty(self, mock_telnet_open, mock_telnet_read_expect, mock_telnet_write,
                                       mock_telnet_read_very_eager, mock_telnet_close):
        ip = '1.1.1.1'
        mock_telnet_read_expect.return_value = ('1', '1', b'response')
        return_result = self.network.connect(ip)
        self.assertTrue(return_result)

    @patch('telnetlib.Telnet.expect')
    @patch('telnetlib.Telnet.open')
    def test_connect_response_is_empty(self, mock_telnet_open, mock_telnet_read_expect):
        ip = '1.1.1.1'
        mock_telnet_open.return_value = True
        mock_telnet_read_expect.return_value = ('1', '1', b'')
        return_result = self.network.connect(ip)
        self.assertFalse(return_result)

    @patch('telnetlib.Telnet.open')
    def test_connect_exception(self, mock_telnet_open):
        ip = '1.1.1.1'
        mock_telnet_open.side_effect = IOError('No route to host')
        return_result = self.network.connect(ip)
        self.assertIsNone(return_result)

    @patch('telnetlib.Telnet.write')
    @patch('telnetlib.Telnet.expect')
    def test_check_login_empty(self, mock_telnet_read_expect, mock_telnet_write):
        login_empty = ''
        login_none = None
        mock_telnet_write.return_value = True
        mock_telnet_read_expect.return_value = ('1', '1', b'Password: ')
        return_result_empty = self.network.login(login_empty)
        return_result_none = self.network.login(login_none)
        self.assertIsNone(return_result_empty)
        self.assertIsNone(return_result_none)

    @patch('telnetlib.Telnet.write')
    @patch('telnetlib.Telnet.expect')
    def test_login_check_no_string_password_in_response(self, mock_telnet_read_expect, mock_telnet_write):
        login = 'admin'
        mock_telnet_write.return_value = True
        mock_telnet_read_expect.return_value = ('1', '1', b'asd: ')
        return_result = self.network.login(login)
        self.assertFalse(return_result)

    @patch('telnetlib.Telnet.write')
    @patch('telnetlib.Telnet.expect')
    def test_login_successfull(self, mock_telnet_read_expect, mock_telnet_write):
        login = 'admin'
        mock_telnet_write.return_value = True
        mock_telnet_read_expect.return_value = ('1', '1', b'Password: ')
        return_result = self.network.login(login)
        self.assertTrue(return_result)

    @patch('telnetlib.Telnet.write')
    @patch('telnetlib.Telnet.expect')
    def test_login_response_is_none(self, mock_telnet_read_expect, mock_telnet_write):
        login = 'admin'
        mock_telnet_write.side_effect = IOError('No route to host')
        mock_telnet_read_expect.return_value = ('1', '1', b'Password: ')
        return_result = self.network.login(login)
        self.assertFalse(return_result)
        mock_telnet_write.side_effect = EOFError('Error reading')
        self.assertFalse(return_result)

    @patch('telnetlib.Telnet.read_very_eager')
    def test_receive_data_not_none(self, mock_telnet_read_very_eager):
        mock_telnet_read_very_eager.return_value = b'data'
        return_result = self.network.recieve_data()
        self.assertTrue(return_result)

    @patch('telnetlib.Telnet.read_very_eager')
    def test_receive_data_is_none_with_exception(self, mock_telnet_read_very_eager):
        mock_telnet_read_very_eager.side_effect = IOError('No route to host')
        return_result = self.network.recieve_data()
        self.assertFalse(return_result)
        mock_telnet_read_very_eager.side_effect = EOFError('Error reading')
        return_result = self.network.recieve_data()
        self.assertFalse(return_result)

    @patch('telnetlib.Telnet.expect')
    def test_receive_data_until_without_exception(self, mock_telnet_expect):
        mock_telnet_expect.return_value = '', '', b'Success'
        list_expect = [b'Success']
        return_result = self.network.receive_data_until(list_expect)
        right_result = b'Success'
        self.assertEqual(right_result, return_result)

    @patch('telnetlib.Telnet.expect')
    def test_receive_data_until_with_exception(self, mock_telnet_expect):
        mock_telnet_expect.side_effect = IOError('No route to host')
        list_expect = [b'Success']
        return_result = self.network.receive_data_until(list_expect)
        right_result = None
        self.assertEqual(right_result, return_result)

    @patch('telnetlib.Telnet.write')
    def test_send_data_success(self, mock_telnet_write):
        sending_data = 'data'
        mock_telnet_write.return_value = True
        return_result = self.network.send_data(sending_data)
        self.assertTrue(return_result)

    @patch('telnetlib.Telnet.write')
    def test_send_data_with_exception(self, mock_telnet_write):
        sending_data = 'data'
        mock_telnet_write.side_effect = IOError('No route to host')
        return_result = self.network.send_data(sending_data)
        self.assertFalse(return_result)
        mock_telnet_write.side_effect = EOFError('Error reading')
        return_result = self.network.send_data(sending_data)
        self.assertFalse(return_result)

    @patch('telnetlib.Telnet.close')
    def test_close_connection_successfull(self, mock_telnet_close):
        mock_telnet_close.return_value = True
        return_result = self.network.close_conection()
        self.assertTrue(return_result)

    @patch('telnetlib.Telnet.close')
    def test_close_connection_with_exception(self, mock_telnet_close):
        mock_telnet_close.side_effect = IOError('No route to host')
        return_result = self.network.close_conection()
        self.assertFalse(return_result)
        mock_telnet_close.side_effect = EOFError('Error reading')
        return_result = self.network.close_conection()
        self.assertFalse(return_result)

    def test_check_ip_empty(self):
        ip_empty = ''
        ip_none = None
        return_result_empty = self.network.check_ip(ip_empty)
        return_result_none = self.network.check_ip(ip_none)
        self.assertFalse(return_result_empty)
        self.assertFalse(return_result_none)

    def test_check_ip_is_normal(self):
        ip = '192.168.111.111'
        return_result = self.network.check_ip(ip)
        self.assertTrue(return_result)
        ip = '19.16.11.11'
        return_result = self.network.check_ip(ip)
        self.assertTrue(return_result)
        ip = '5.168.0.11'
        return_result = self.network.check_ip(ip)
        self.assertTrue(return_result)

    def test_check_ip_more_4_oktets(self):
        ip = '1.1.1.1.1'
        return_result = self.network.check_ip(ip)
        self.assertFalse(return_result)

    def test_check_ip_more_3_numbers_in_oktet(self):
        ip = '1111.1.1111.111111'
        return_result = self.network.check_ip(ip)
        self.assertFalse(return_result)
