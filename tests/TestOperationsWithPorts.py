import unittest
from unittest.mock import patch

from Controllers.ControllerMain import ControllerMain
from Controllers.OperationsWithPorts import OperationsWithPorts


class MyTestCase(unittest.TestCase):

    def setUp(self):
        controller = ControllerMain('')
        self.args = {'parameter': 'dlink_backup', 'ip_range': '172.1.2.80,172.1.2.82',
                     'ip_dst_for_backup': '10.6.224.3',
                     'path_work_directory': '/Users/toxa/PycharmProjects/dlink_utility/'}
        self.operations_with_ports = OperationsWithPorts(controller)

    @patch('sys.exit')
    @patch('Controllers.ControllerMain.ControllerMain.get_dlink_model')
    @patch('Controllers.ControllerMain.ControllerMain.network_close_connection')
    @patch('Controllers.ControllerMain.ControllerMain.authorisation')
    @patch('Controllers.ControllerMain.ControllerMain.network_send_data')
    @patch('Controllers.ControllerMain.ControllerMain.network_receive_data_until')
    def test_get_mac_on_port_correct_mac(self, mock_receive_data_until, mock_send_data, mock_authorisation,
                                         mock_close_connection, mock_get_dlink_model, mock_sys_exit):
        mock_receive_data_until.return_value = b'kjhkjhskdf00-C0-34-DA-00-00'
        mock_send_data.return_value = True
        mock_authorisation.return_value = True
        mock_close_connection.return_value = True
        ip_address = '192.168.1.1'
        args = {'ports': '0-20'}
        mock_get_dlink_model.return_value = 'DGS-1210-10P/ME'
        mock_sys_exit.return_value = True
        correct_answer = {1: ['00-C0-34-DA-00-00']}
        mac_list = self.operations_with_ports.get_mac_on_port(ip_address, args)
        self.assertEqual(correct_answer, mac_list)

    def test_match_mac_from_response_correct(self):
        response_from_switch = b'sdfafdg 00-cd-34-da-89-43kjhkjhskdf00-C0-34-DA-00-00\n00-C0-34-DA-00-00'
        correct_return = ['00-cd-34-da-89-43', '00-C0-34-DA-00-00', '00-C0-34-DA-00-00']
        mac_address_list = self.operations_with_ports.match_mac_from_response(response_from_switch)
        self.assertEqual(correct_return, mac_address_list)

    def test_match_mac_from_response_incorrect(self):
        response_from_switch = b'sdfaf0-3'
        mac_address_list = self.operations_with_ports.match_mac_from_response(response_from_switch)
        self.assertFalse(mac_address_list)

    def test_get_ports_number_from_model(self):
        model = 'DGS-1210-28P/ME'
        correct_answer = 28
        ports_numbers = self.operations_with_ports.get_ports_number_from_model(model)
        self.assertEqual(correct_answer, ports_numbers)

    def test_check_port_range_correct(self):
        ports_range = '3-10'
        ports_range_answer = [3, 10]
        ports_range_checked = self.operations_with_ports.check_port_range(ports_range)
        self.assertEqual(ports_range_answer, ports_range_checked)

    def test_check_port_range_with_string(self):
        ports_range = 'rq'
        ports_range_checked = self.operations_with_ports.check_port_range(ports_range)
        self.assertFalse(ports_range_checked)
        ports_range = '3-q'
        ports_range_checked = self.operations_with_ports.check_port_range(ports_range)
        self.assertFalse(ports_range_checked)

    def test_check_port_range_with_one_port(self):
        ports_range = '3'
        ports_range_answer = [3, 4]
        ports_range_checked = self.operations_with_ports.check_port_range(ports_range)
        self.assertEqual(ports_range_answer, ports_range_checked)

    def test_check_port_range_with_zero(self):
        ports_range = '0'
        ports_range_answer = [1, 2]
        ports_range_checked = self.operations_with_ports.check_port_range(ports_range)
        self.assertEqual(ports_range_answer, ports_range_checked)


if __name__ == '__main__':
    unittest.main()
