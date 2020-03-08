import unittest
from unittest.mock import patch
from MainView import MainView


class TestGeneral(unittest.TestCase):

    # @patch('multiprocessing.Process.start', new=lambda x: None)
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    @patch('Model.Model.get_dlink_model')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.write_to_log_file')
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
