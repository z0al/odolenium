#! python3
# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from odolenium.widgets.db import DatabaseWidget
import odolenium.util as util
import odolenium.wait as wait


class LoginWidget(object):
    allowed_urls = [
        "/web/login",
        "/web/database/manager",
        "/web/database/selector"
    ]
    def __init__(self,driver, server_ver):

        self.url =  util.parse_url(driver.current_url)

        assert self.url.path.rstrip("/") in LoginWidget.allowed_urls

        self.driver = driver
        self.ver = server_ver

    def login(self, user, password, db):
        db_wdgt = DatabaseWidget(self.driver, self.ver)
        db_wdgt.select_db(db)

        with wait.for_page_load(self.driver):
            # fill in login form.
            login_field = self.driver.find_element(By.ID, u"login")
            login_field.send_keys(user)
            password_field = self.driver.find_element(By.ID, u"password")
            password_field.send_keys(password)
            login_button = self.driver.find_element(
                By.CSS_SELECTOR,
                ".btn.btn-primary[type='submit']"
            )
            login_button.click()
