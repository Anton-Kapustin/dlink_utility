import unittest
from unittest.mock import patch

from MainView import MainView


class TestGeneral(unittest.TestCase):

    # @patch('multiprocessing.Process.start', new=lambda x: None)
    @patch('Controllers.ControllerMain.ControllerMain.network_send_data')
    @patch('Controllers.ControllerMain.ControllerMain.network_receive_data_until')
    @patch('Model.Model.get_dlink_model')
    @patch('Controllers.ControllerMain.ControllerMain.authorisation')
    @patch('Controllers.ControllerMain.ControllerMain.write_to_log_file')
    def test_backup(self, mock_write_to_log_file, mock_controller_authorisation, mock_model_get_dlink_model,
                    mock_network_receive_data_until, mock_network_send_data):
        argv = ('/Users/toxa/PycharmProjects/dlink_utility/', 'dlink_backup', '172.1.2.80,172.1.2.81', '10.6.224.1')
        mock_write_to_log_file.return_value = True
        mock_controller_authorisation.return_value = True
        mock_model_get_dlink_model.return_value = 'DGS-3200'
        mock_network_receive_data_until.return_value = b'success'
        mock_network_send_data.return_value = 'success'
        view = MainView(argv)
        self.assertTrue(view)

    @patch('Model.Model.get_mac_on_ports')
    @patch('Controllers.ControllerMain.ControllerMain.file_settings_exists')
    @patch('Controllers.ControllerMain.ControllerMain.network_send_data')
    @patch('Controllers.ControllerMain.ControllerMain.network_receive_data_until')
    @patch('Model.Model.get_dlink_model')
    @patch('Controllers.ControllerMain.ControllerMain.authorisation')
    @patch('Controllers.ControllerMain.ControllerMain.write_to_log_file')
    def test_backup(self, mock_write_to_log_file, mock_controller_authorisation, mock_model_get_dlink_model,
                    mock_network_receive_data_until, mock_network_send_data, mock_file_settings_exists,
                    mock_get_mac_on_ports):
        argv = ('/Users/toxa/PycharmProjects/dlink_utility/', 'mac_on_port', '172.1.2.80,172.1.2.81', '1-2')
        mock_write_to_log_file.return_value = True
        mock_controller_authorisation.return_value = True
        mock_model_get_dlink_model.return_value = 'DGS-1210-10P/ME'
        mock_network_receive_data_until.return_value = b'kjhkjhskdf00-C0-34-DA-00-00'
        mock_network_send_data.return_value = 'success'
        mock_file_settings_exists.return_value = True
        mock_get_mac_on_ports.return_value = {'192.168.1.2': {2:['00-11-22-df-ab-ac', '00-11-22-df-ab-ac'],
                                                              3: ['00-11-22-df-ab-ac']},
                                              '192.168.1.3': {4: ['00-11-22-df-ab-ac']}}
        view = MainView(argv)
        self.assertTrue(view)
