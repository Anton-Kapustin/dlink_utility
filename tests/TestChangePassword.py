import unittest
from unittest.mock import patch

from ChangePassword import ChangePassword
from ControllerMain import ControllerMain


class TestChangePassword(unittest.TestCase):

    def setUp(self) -> None:
        self.controllerMain = ControllerMain('')
        self.changePassword = ChangePassword('')

    @patch('')
    def test_dlink_mass_send_command(self):
        cmd = 'cmd'
        ip_addrass = '172.1.2.86'
        model = 'DGS-1210-10P/ME'

