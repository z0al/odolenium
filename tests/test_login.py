#! python3
from selenium.webdriver import Firefox
import pytest
import unittest
import os

from odolenium import *

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.ui = OdooUI(
            Firefox(),
            {
                'url': 'http://localhost:9000',
                'admin_password':'admin',
                'log_level':'INFO'
            }
        )

    def test_one(self):
        self.ui.login('admin','admin','db1')
        assert self.ui.driver.current_url.startswith('http://localhost:9000/web')

    def test_two(self):
        try:
            self.ui.login('admin','admin','db2')
        except OdoleniumError:
            assert True


    def tearDown(self):
        self.ui.driver.quit()



