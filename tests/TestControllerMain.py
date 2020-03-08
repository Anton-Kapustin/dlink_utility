import unittest
from datetime import datetime
from unittest.mock import patch

from ControllerDlinkBackup import ControllerDlinkBackup
from ControllerMain import ControllerMain


class TestControllerMain(unittest.TestCase):

    def setUp(self):
        self.controller = ControllerMain('')

    @patch('ControllerMain.ControllerMain.network_send_data')
    @patch('ControllerMain.ControllerMain.network_receive_data_until')
    @patch('Model.Model.get_dlink_model')
    @patch('ControllerMain.ControllerMain.authorisation')
    def test_create_async_process_from_ip_range(self, mock_authorisation, mock_get_dlink_model,
                                                mock_controller_receive_data_until, mock_controller_send_data):
        mock_authorisation.return_value = True
        mock_get_dlink_model.return_value = 'DGS-1210-10P/ME'
        mock_controller_receive_data_until.return_value = b'Success'
        mock_controller_send_data.return_value = True
        ip_range = ('172.1.0.0', '172.1.0.150')
        dlink_backup = ControllerDlinkBackup(self.controller)
        args = {'parameter': 'dlink_backup', 'ip_range': '172.1.2.80,172.1.2.82',
                'ip_dst_for_backup': '10.6.224.3',
                'path_work_directory': '/Users/toxa/PycharmProjects/dlink_utility/'}
        return_result = self.controller.create_async_network_processes_from_ip_range(args,
                                                                                     dlink_backup.make_dlink_backup)

    # ==================================================================================================================
    # Test Authorisation
    # ==================================================================================================================

    @patch('Model.Model.get_password_list')
    @patch('Network.Network.connect')
    @patch('Network.Network.login')
    def test_authorisation_with_dlink_auccessful(self, mock_network_login, mock_network_connect, mock_get_password_list):
        mock_network_connect.return_value = b'DGS-1210-10P/ME UserName:'
        mock_network_login.return_value = b'DGS-1210-10P/ME:5#'
        mock_get_password_list.return_value = ['1', '2']
        ip_address = '172.1.0.12'
        result_from_connect = self.controller.authorisation(ip_address)
        self.assertTrue(result_from_connect)

    @patch('Model.Model.get_password_list')
    @patch('Network.Network.connect')
    @patch('Network.Network.login')
    def test_authorisation_with_dlink_incorrect_login(self, mock_network_login, mock_network_connect, mock_get_password_list):
        mock_network_connect.return_value = b'DGS-1210-10P/ME UserName:'
        mock_network_login.return_value = b'Incorrect'
        mock_get_password_list.return_value = ['1', '2']
        ip_address = '172.1.0.12'
        result_from_connect = self.controller.authorisation(ip_address)
        self.assertFalse(result_from_connect)
        mock_network_login.return_value = b'failed'
        result_from_connect = self.controller.authorisation(ip_address)
        self.assertFalse(result_from_connect)

    @patch('Model.Model.get_password_list')
    @patch('Network.Network.connect')
    @patch('Network.Network.login')
    def test_authorisation_with_dlink_incorrect_response_from_connect(self, mock_network_login, mock_network_connect, mock_get_password_list):
        mock_network_connect.return_value = b'dangerfield'
        mock_network_login.return_value = b'DGS-1210-10P/ME:5#'
        mock_get_password_list.return_value = ['1', '2']
        ip_address = '172.1.0.12'
        result_from_connect = self.controller.authorisation(ip_address)
        self.assertFalse(result_from_connect)

    @patch('Model.Model.get_password_list')
    @patch('Network.Network.connect')
    @patch('Network.Network.login')
    def test_authorisation_with_dlink_incorrect_response_from_login(self, mock_network_login, mock_network_connect, mock_get_password_list):
        mock_network_connect.return_value = b'DGS-1210-10P/ME UserName:'
        mock_network_login.return_value = b'sdfk;lsdf'
        mock_get_password_list.return_value = ['1', '2']
        ip_address = '172.1.0.12'
        result_from_connect = self.controller.authorisation(ip_address)
        self.assertFalse(result_from_connect)

    @patch('Model.Model.get_password_list')
    @patch('Network.Network.connect')
    @patch('Network.Network.login')
    def test_authorisation_with_dlink_incorrect_password(self, mock_network_login, mock_network_connect, mock_get_password_list):
        mock_network_connect.return_value = b'DGS-1210-10P/ME UserName:'
        mock_network_login.return_value = b'incorrect'
        mock_get_password_list.return_value = ['1', '2']
        ip_address = '172.1.0.12'
        result_from_connect = self.controller.authorisation(ip_address)
        self.assertFalse(result_from_connect)

    # ==================================================================================================================
    # Test Make NETWORK Address
    # ==================================================================================================================

    def test_make_network_address_third_octet_in_ip_range_static(self):
        ip_range = ('172.1.0.0', '172.1.0.150')
        return_result = self.controller.make_network_address(ip_range)
        self.assertTrue(return_result)
        self.assertTrue('172.1.0.3' in return_result)
        self.assertTrue('172.1.0.150' in return_result)
        self.assertFalse('172.1.0.0' in return_result)
        self.assertFalse('172.1.0.151' in return_result)
        self.assertFalse('172.1.1.6' in return_result)

    def test_make_network_address_start_octet_large_end_octet(self):
        ip_range = ('172.1.0.50', '172.1.0.3')
        return_result = self.controller.make_network_address(ip_range)
        self.assertFalse(return_result)

    def test_make_network_address_third_octet_different_and_last_octet_in_end_range_large_start_range(self):
        ip_range = ('172.1.0.0', '172.1.1.5')
        return_result = self.controller.make_network_address(ip_range)
        self.assertTrue(return_result)
        self.assertTrue('172.1.0.1' in return_result)
        self.assertTrue('172.1.0.254' in return_result)
        self.assertTrue('172.1.1.1' in return_result)
        self.assertTrue('172.1.1.5' in return_result)
        self.assertFalse('172.1.0.255' in return_result)
        self.assertFalse('172.1.1.6' in return_result)

    def test_make_network_address_third_octet_different_and_last_octet_in_start_range_large_end_range(self):
        ip_range = ('172.1.2.0', '172.1.1.5')
        return_result = self.controller.make_network_address(ip_range)
        self.assertFalse(return_result)

    # ==================================================================================================================
    # Test Make Network Gateway Address For Dlink Backup
    # ==================================================================================================================

    def test_make_network_gateway_address(self):
        ip_range = ('172.1.0.0', '172.1.1.5')
        return_result = self.controller.make_network_gateway_address(ip_range)
        gateway_address = return_result
        correct_gateway_address = '172.1.1.254'
        self.assertEqual(gateway_address, correct_gateway_address)

    # ==================================================================================================================
    # Test Check IP Range Correct
    # ==================================================================================================================

    def test_check_ip_range_is_correct(self):
        ip_range = ('172.1.2.80', '172.1.2.81')
        start_ip_range = ip_range[0]
        end_ip_range = ip_range[1]
        start_ip_range_splited = start_ip_range.split('.')
        end_ip_range_splited = end_ip_range.split('.')
        third_octet_in_start_ip_range = int(start_ip_range_splited[2])
        third_octet_in_end_ip_range = int(end_ip_range_splited[2])
        last_octet_in_start_ip_range = int(start_ip_range_splited[3])
        last_octet_in_end_ip_range = int(end_ip_range_splited[3])
        return_result = self.controller.check_ip_range_correct(third_octet_in_start_ip_range,
                                                               third_octet_in_end_ip_range,
                                                               last_octet_in_start_ip_range,
                                                               last_octet_in_end_ip_range)
        self.assertTrue(return_result)

    def test_check_ip_range_is_incorrect(self):
        ip_range = ('172.1.1.0', '172.1.0.5')
        start_ip_range = ip_range[0]
        end_ip_range = ip_range[1]
        start_ip_range_splited = start_ip_range.split('.')
        end_ip_range_splited = end_ip_range.split('.')
        third_octet_in_start_ip_range = int(start_ip_range_splited[2])
        third_octet_in_end_ip_range = int(end_ip_range_splited[2])
        last_octet_in_start_ip_range = int(start_ip_range_splited[3])
        last_octet_in_end_ip_range = int(end_ip_range_splited[3])
        return_result = self.controller.check_ip_range_correct(third_octet_in_start_ip_range,
                                                               third_octet_in_end_ip_range,
                                                               last_octet_in_start_ip_range,
                                                               last_octet_in_end_ip_range)
        self.assertFalse(return_result)

    # ==================================================================================================================
    # Test Check Switch Model
    # ==================================================================================================================

    def test_check_hp_model(self):
        checking_string = b"\x1b[2J\x1b[?7l\x1b[3;23r\x1b[?6l\x1b[1;1H\x1b[?25l\x1b[1;1HProCurve J9019B Switch " \
                          b"2510B-24\r\n\rSoftware revision Q.11.57\r\n\r\r\n\rCopyright (C) 1991-2012 Hewlett-Packard " \
                          b"Co.  All Rights Reserved.\n\r\n\r                           RESTRICTED RIGHTS " \
                          b"LEGEND\n\r\n\r Use, duplication, or disclosure by the Government is subject to " \
                          b"restrictions\n\r as set forth in subdivision (b) (3) (ii) of the Rights in Technical " \
                          b"Data and\n\r Computer Software clause at 52.227-7013.\n\r\n\r         HEWLETT-PACKARD " \
                          b"COMPANY, 3000 Hanover St., Palo Alto, CA 94303\n\r\n\rWe'd like to keep you up to date " \
                          b"about:\n\r  * Software feature updates\n\r  * New product announcements\n\r  * Special " \
                          b"events\n\r\n\rPlease register your products now at:  www.ProCurve.com\n\r\n\r\n\r\x1b" \
                          b"[24;1HPress any key to continue\x1b[1;1H\x1b[?25h\x1b[24;27H"

        return_result = self.controller.check_switch_model(checking_string)
        self.assertFalse(return_result)

    def test_check_dlink_response(self):
        response_from_dlink = b'\x1b[H\x1b[J\r\x1b[100B\x1b[H\x1b[J\r\x1b[100B\r\n                    DGS-1210-10P/ME' \
                              b' Gigabit Ethernet Switch\r\n                            Command Line Interface' \
                              b'\r\n\r\n                           Firmware: Build 7.02.B010\r\n             ' \
                              b'Copyright(C) 2012 D-Link Corporation. All rights reserved.\r\n\r\nUserName: '
        return_result = self.controller.check_switch_model(response_from_dlink)
        self.assertTrue(return_result)

    # ==================================================================================================================

    def test_is_web_smart_model_true(self):
        dlink_model = 'DGS-1210-10P'
        return_result = self.controller.is_web_smart_model(dlink_model)
        self.assertTrue(return_result)

    def test_is_web_smart_model_false(self):
        dlink_model = 'DGS-1210-10P/ME'
        return_result = self.controller.is_web_smart_model(dlink_model)
        self.assertFalse(return_result)
        dlink_model = 'DGS-3120-24SC'
        return_result = self.controller.is_web_smart_model(dlink_model)
        self.assertFalse(return_result)

    def test_returning_date_in_string(self):
        date_now = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        return_result = self.controller.get_date_in_string()
        self.assertEqual(date_now, return_result)

    def test_delete_last_object_in_path(self):
        checking_path = '/Users/toxa/PycharmProjects/dlink_utility/MainView.py'
        result = self.controller.delete_last_object_in_path(checking_path)
        right_result = '/Users/toxa/PycharmProjects/dlink_utility/'
        self.assertEqual(right_result, result)
        checking_path = '/Users/toxa/PycharmProjects/dlink_utility/'
        right_result = '/Users/toxa/PycharmProjects/'
        result = self.controller.delete_last_object_in_path(checking_path)
        self.assertEqual(right_result, result)
        checking_path = '/Users/toxa/PycharmProjects/dlink-utility/'
        right_result = '/Users/toxa/PycharmProjects/'
        result = self.controller.delete_last_object_in_path(checking_path)
        self.assertEqual(right_result, result)

    @patch('builtins.open', unittest.mock.mock_open(read_data='open'))
    @patch('os.write')
    @patch('os.close')
    @patch('os.stat')
    @patch('os.mkdir')
    def test_write_to_log_file(self, mock_os_mkdir, mock_os_stat, mock_os_close, mock_os_write):
        mock_os_mkdir.return_value = True
        mock_os_stat.return_value = 'stat'
        mock_os_close.return_value = True
        mock_os_write.return_value = True
        path = '/Users/toxa/PycharmProjects/dlink_utility/'
        string_write = 'write'
        write_parameter = 'a+'
        return_result = self.controller.write_to_log_file(path, string_write, write_parameter)
        self.assertTrue(return_result)

    def test_check_string_contain_item_from_list(self):
        list_read_expect = [b'Success', b'success', b'successful', b'fail', b'Fail']
        return_result = self.controller.check_string_contain_item_from_list(list_read_expect[3], list_read_expect)
        self.assertEqual(list_read_expect[3].decode('utf-8'), return_result)

    @patch('json.load')
    @patch('os.stat')
    @patch('builtins.open')
    def test_filesettings_exists_login_no_empty(self, mock_open, mock_os_stat, mock_json_load):
        mock_open.return_value = {"login": "admin", "password": ["1", "2"]}
        mock_os_stat.return_value = True
        mock_json_load.return_value = {"login": "admin", "password": ["1", "2"]}
        return_result = self.controller.file_settings_exists('../settings')
        self.assertTrue(return_result)

    @patch('json.load')
    @patch('os.stat')
    @patch('builtins.open')
    def test_filesettings_exists_login_empty(self, mock_open, mock_os_stat, mock_json_load):
        mock_open.return_value = {"login": "", "password": ""}
        mock_os_stat.return_value = True
        mock_json_load.return_value = {"login": "", "password": ""}
        return_result = self.controller.file_settings_exists('../settings')
        self.assertFalse(return_result)

    @patch('json.load')
    @patch('os.stat')
    @patch('builtins.open')
    def test_filesettings_exists_empty(self, mock_open, mock_os_stat, mock_json_load):
        mock_open.return_value = {"login": "", "password": ""}
        mock_os_stat.return_value = True
        mock_json_load.return_value = {"login": "", "password": ""}
        return_result = self.controller.file_settings_exists('../settings')
        self.assertFalse(return_result)

    # def test_real_filesettings_exists_file_empty(self):
    #     return_result = self.controller.file_settings_exists('../settings')
    #     self.assertFalse(return_result)
