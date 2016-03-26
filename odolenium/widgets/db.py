#! python3
# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

import odolenium.util as util
import odolenium.wait as wait


class DatabaseWidget(object):
    db_urls = [
        # v9
        "/web/database/manager",
        "/web/database/selector"
    ]

    def __init__(self, driver, server_ver):
        self.driver = driver
        self.ver = server_ver
        self.url = util.parse_url(driver.current_url)

    def select_db(self, name):
        # v9
        if self.ver.startswith("9.0"):
            if self.url.path.rstrip("/") not in DatabaseWidget.db_urls:
                _url = util.urlgen(self.url, "/web/database/selector")
                self.driver.get(_url)

            with wait.for_page_load(self.driver):
                db_list = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".o_database_list .list-group .list-group-item"
                )

                for db in db_list:
                    if db.text == name:
                        db.click()
                        break
        # v8
        elif self.ver.startswith("8.0"):
            raise NotImplementedError

        # v7
        elif self.ver.startswith("7.0"):
            raise NotImplementedError
