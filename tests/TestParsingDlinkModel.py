import unittest

from ControllerMain import ControllerMain


class TestParsingDlinkModelName(unittest.TestCase):

    def setUp(self):
        self.controller_main = ControllerMain('')

    def test_1210_10pme(self):
        true_dlink_model_name = 'DGS-1210-10P/ME'
        raw_response_with_model_name = b'\x1b[H\x1b[J\r\x1b[100B\x1b[H\x1b[J\r\x1b[100B\r\n                    ' \
                                       b'DGS-1210-10P/ME' \
                                       b' Gigabit Ethernet Switch\r\n                          Command Line Interface' \
                                       b'\r\n\r\n                         Firmware: Build 7.02.B010\r\n             ' \
                                       b'Copyright(C) 2012 D-Link Corporation. All rights reserved.\r\n\r\nUserName: '
        dlink_model_name_parced = self.controller_main.parse_dlink_model_name(raw_response_with_model_name)
        self.assertEqual(dlink_model_name_parced, true_dlink_model_name)

    def test_1210_10p(self):
        true_dlink_model_name = 'DGS-1210-10P'
        raw_response_with_model_name = b'\x1b[H\x1b[J\r\x1b[100B\x1b[H\x1b[J\r\x1b[100B\r\n                    ' \
                                       b'DGS-1210-10P' \
                                       b' Gigabit Ethernet Switch\r\n                          Command Line Interface' \
                                       b'\r\n\r\n                         Firmware: Build 7.02.B010\r\n             ' \
                                       b'Copyright(C) 2012 D-Link Corporation. All rights reserved.\r\n\r\nUserName: '
        controllder = ControllerMain(self.controller_main)
        dlink_model_name_parced = self.controller_main.parse_dlink_model_name(raw_response_with_model_name)
        self.assertEqual(dlink_model_name_parced, true_dlink_model_name)

    def test_1210_28p(self):
        true_dlink_model_name = 'DES-1210-28P'
        raw_response_with_model_name = b'\x1b[H\x1b[J\r\x1b[100B\x1b[H\x1b[J\r\x1b[100B\r\n                    ' \
                                       b'DES-1210-28P' \
                                       b' Gigabit Ethernet Switch\r\n                          Command Line Interface' \
                                       b'\r\n\r\n                         Firmware: Build 7.02.B010\r\n             ' \
                                       b'Copyright(C) 2012 D-Link Corporation. All rights reserved.\r\n\r\nUserName: '
        controllder = ControllerMain(self.controller_main)
        dlink_model_name_parced = self.controller_main.parse_dlink_model_name(raw_response_with_model_name)
        self.assertEqual(dlink_model_name_parced, true_dlink_model_name)

    def test_1210_28pme(self):
        true_dlink_model_name = 'DGS-1210-28P/ME'
        raw_response_with_model_name = b'\x1b[H\x1b[J\r\x1b[100B\x1b[H\x1b[J\r\x1b[100B\r\n                    ' \
                                       b'DGS-1210-28P/ME' \
                                       b' Gigabit Ethernet Switch\r\n                          Command Line Interface' \
                                       b'\r\n\r\n                         Firmware: Build 7.02.B010\r\n             ' \
                                       b'Copyright(C) 2012 D-Link Corporation. All rights reserved.\r\n\r\nUserName: '
        controllder = ControllerMain(self.controller_main)
        dlink_model_name_parced = self.controller_main.parse_dlink_model_name(raw_response_with_model_name)
        self.assertEqual(dlink_model_name_parced, true_dlink_model_name)

    def test_1510_28pme(self):
        true_dlink_model_name = 'DGS-1510-28LP/ME'
        raw_response_with_model_name = b'\x1b[H\x1b[J\r\x1b[100B\x1b[H\x1b[J\r\x1b[100B\r\n                    ' \
                                       b'DGS-1510-28LP/ME' \
                                       b' Gigabit Ethernet Switch\r\n                          Command Line Interface' \
                                       b'\r\n\r\n                         Firmware: Build 7.02.B010\r\n             ' \
                                       b'Copyright(C) 2012 D-Link Corporation. All rights reserved.\r\n\r\nUserName: '
        controllder = ControllerMain(self.controller_main)
        dlink_model_name_parced = self.controller_main.parse_dlink_model_name(raw_response_with_model_name)
        self.assertEqual(dlink_model_name_parced, true_dlink_model_name)

    def test_DGS_3120_24SC(self):
        true_dlink_model_name = 'DGS-3120-24SC'
        raw_response_with_model_name = b'\x1b[0m\x1b[1;1H\x1b[2J\n\r    DGS-3120-24SC Gigabit Ethernet Switch\n\r ' \
                                       b'                           Command Line Interface\n\r\n\r ' \
                                       b'Firmware: Build 4.11.R006\n\r         Copyright(C) 2016 D-Link Corporation.' \
                                       b' All rights reserved.\n\rUserName:'
        controllder = ControllerMain(self.controller_main)
        dlink_model_name_parced = self.controller_main.parse_dlink_model_name(raw_response_with_model_name)
        self.assertEqual(dlink_model_name_parced, true_dlink_model_name)
