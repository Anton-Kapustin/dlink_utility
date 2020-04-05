import re
import unittest
from unittest.mock import patch

from ControllerDlinkBackup import ControllerDlinkBackup
from ControllerMain import ControllerMain


class TestControllerDlinkBackup(unittest.TestCase):

    def setUp(self):
        self.controllerMain = ControllerMain('')
        self.args = {'parameter'          : 'dlink_backup', 'ip_range': '172.1.2.80,172.1.2.82',
                     'ip_dst_for_backup'  : '10.6.224.3',
                     'path_work_directory': '/Users/toxa/PycharmProjects/dlink_utility/'}
        self.controllerDlinkBackup = ControllerDlinkBackup(self.controllerMain)

    # ==================================================================================================================
    # Test Make Dlink Backup
    # ==================================================================================================================

    @patch('ControllerMain.ControllerMain.network_close_connection')
    @patch('ControllerMain.ControllerMain.write_to_log_file')
    @patch('ControllerDlinkBackup.ControllerDlinkBackup.make_cmd_for_backup_for_different_dlink_switches')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    @patch('sys.exit')
    def test_make_dlink_backup_with_fake_network_successful_result(self, mock_sys_exit, mock_network_receive_data_until,
                                                                   mock_network_send_data,
                                                                   mock_controller_authorisation,
                                                                   mock_make_cmd_for_backup, mock_write_to_log_file,
                                                                   mock_close_connection):
        mock_close_connection.return_value = True
        mock_network_send_data.return_value = True
        mock_network_receive_data_until.return_value = b'success'
        mock_sys_exit.return_value = True
        mock_controller_authorisation.return_value = True
        mock_write_to_log_file.return_value = True
        mock_make_cmd_for_backup.return_value = 'q'
        ip_address = '172.1.0.18'
        return_result = self.controllerDlinkBackup.make_dlink_backup(ip_address, self.args)
        self.assertIsNone(return_result)

    @patch('ControllerMain.ControllerMain.network_close_connection')
    @patch('ControllerDlinkBackup.ControllerDlinkBackup.make_cmd_for_backup_for_different_dlink_switches')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('sys.exit')
    def test_make_dlink_backup_with_fake_network_unsucceess_result(self, mock_sys_exit, mock_network_send_data,
                                                                   mock_controller_authorisation,
                                                                   mock_make_cmd_for_backup, mock_close_connection):
        mock_network_send_data.return_value = True
        mock_sys_exit.return_value = True
        mock_controller_authorisation.return_value = True
        mock_make_cmd_for_backup.return_value = ''
        mock_close_connection.return_value = True
        ip_address = '172.1.0.14'
        return_result = self.controllerDlinkBackup.make_dlink_backup(ip_address, self.args)
        self.assertFalse(return_result)

    @patch('ControllerMain.ControllerMain.network_close_connection')
    @patch('ControllerMain.ControllerMain.check_folder_exists')
    @patch('Model.Model.get_dlink_model')
    @patch('ControllerMain.ControllerMain.write_to_log_file')
    @patch('ControllerDlinkBackup.ControllerDlinkBackup.make_cmd_for_backup_for_different_dlink_switches')
    @patch('ControllerMain.ControllerMain.authorisation')
    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    @patch('sys.exit')
    def test_make_dlink_backup_with_fake_network_write_to_log_with_nonetype_response(self, mock_sys_exit,
                                                                                     mock_network_receive_data_until,
                                                                                     mock_network_send_data,
                                                                                     mock_controller_authorisation,
                                                                                     mock_make_cmd_for_backup,
                                                                                     mock_write_to_log_file,
                                                                                     mock_get_dlink_model,
                                                                                     mock_check_folder_exists,
                                                                                     mock_close_connection):
        mock_network_send_data.return_value = True
        mock_network_receive_data_until.return_value = None
        mock_sys_exit.return_value = True
        mock_controller_authorisation.return_value = True
        mock_write_to_log_file.return_value = True
        mock_make_cmd_for_backup.return_value = 'q'
        mock_get_dlink_model.return_value = 'DGS'
        mock_check_folder_exists.return_value = True
        mock_close_connection.return_value = True
        ip_address = '172.1.0.14'
        return_result = self.controllerDlinkBackup.make_dlink_backup(ip_address, self.args)
        self.assertIsNone(return_result)

    def test_make_cmd_for_backup_for_different_dlink_switches_for_1210_series_me(self):
        dlink_model = 'DGS-1210-10P/ME'
        ip_address = '172.1.0.123'
        ip_dst_for_backup = '10.2.224.1'
        string_with_date = self.controllerMain.get_date_in_string()
        return_result = self.controllerDlinkBackup.make_cmd_for_backup_for_different_dlink_switches(dlink_model,
                                                                                                    ip_address,
                                                                                                    ip_dst_for_backup)
        true_cmd = 'upload cfg_toTFTP ' + ip_dst_for_backup + ' ' + ip_address + '\\' + ip_address + \
                   '_' + re.sub('[/]', '', dlink_model) + '_' + string_with_date + '.cfg\n'
        self.assertEqual(true_cmd, return_result)
        dlink_model = 'DGS-1210-28P/ME'
        return_result = self.controllerDlinkBackup.make_cmd_for_backup_for_different_dlink_switches(dlink_model,
                                                                                                    ip_address,
                                                                                                    ip_dst_for_backup)
        true_cmd = 'upload cfg_toTFTP ' + ip_dst_for_backup + ' ' + ip_address + '\\' + ip_address + \
                   '_' + re.sub('[/]', '', dlink_model) + '_' + string_with_date + '.cfg\n'
        self.assertEqual(true_cmd, return_result)

    def test_make_cmd_for_backup_for_different_dlink_switches_for_web_smart(self):
        dlink_model = 'DGS-1210-10P'
        ip_address = '172.1.0.123'
        ip_dst_for_backup = '10.2.224.1'
        return_result = self.controllerDlinkBackup.make_cmd_for_backup_for_different_dlink_switches(dlink_model,
                                                                                                    ip_address,
                                                                                                    ip_dst_for_backup)
        string_with_date = self.controllerMain.get_date_in_string()
        true_cmd = 'upload cfg_toTFTP ' + ip_dst_for_backup + ' ' + ip_address + '\\' + ip_address + \
                   '_' + re.sub('[/]', '', dlink_model) + '_' + string_with_date + '\n'
        self.assertEqual(true_cmd, return_result)
        dlink_model = 'DGS-1210-28P'
        return_result = self.controllerDlinkBackup.make_cmd_for_backup_for_different_dlink_switches(dlink_model,
                                                                                                    ip_address,
                                                                                                    ip_dst_for_backup)
        true_cmd = 'upload cfg_toTFTP ' + ip_dst_for_backup + ' ' + ip_address + '\\' + ip_address + \
                   '_' + re.sub('[/]', '', dlink_model) + '_' + string_with_date + '\n'
        self.assertEqual(true_cmd, return_result)
