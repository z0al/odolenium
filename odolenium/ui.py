#! python3
# -*- coding: utf-8 -*-
import contextlib

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from erppeek import Client, Error

import odolenium.util as util
import odolenium.widgets as widgets
from .error import *
from .conf import *
from . import wait

# Supported Odoo server versions
versions = ["9.0c"]

class OdooUI(object):

    def __init__(self, driver, config):
        self.driver = driver
        self.setup(config)

        self.url = util.parse_url(self.config["url"])

        if self.url is None:
            raise OdoleniumError("'{}' isn't valid URL".format(self.config["url"]))

        log.info("Setting up XML-RPC connection to {}".format(self.urlgen()))
        try:
            self.rpc = Client(self.url.geturl())
            log.info("Connection succeed")
        except:
            log.error("Connection failed")
            raise ConnectionRefusedError("Can't connect to Odoo server")

        self.ver = self.rpc.db.server_version()
        log.info("Found version {} Odoo server".format(self.ver))

        if self.ver not in versions:
            raise OdoleniumError("Unsupported Odoo version '{}'".format(self.ver))

    def login(self, user, password, db):
        """
        Login to Odoo server using given user and password and database.
        """
        log.info("Trying to log in over XML-RPC")
        self.rpc_login(user, password, db)

        # get first page
        log.info("GET {}".format(self.url.geturl()))
        self.driver.get(self.url.geturl())

        # login from web UI
        login_w = widgets.LoginWidget(self.driver, self.ver)
        login_w.login(user, password, db)

    def setup(self,config):
        """
        Setup configration
        """
        self.config = loadconfig(config)

    def urlgen(self, path=""):
        """
        Generate URL.
        """
        return util.urlgen(self.url, path)

    def rpc_login(self, user, password, db):
        """
        Setup XML-RPC connection using given credentials
        """
        try:
            self.rpc.login(user,password,db)
        except Error as er: # erppeek.Error
            log.critical("{}".format(er))
            raise OdoleniumError("{}".format(er))

        log.info("Logged in as '{}' to database '{}'".format(self.rpc.user, db))

        log.info("Searching for 'web_selenium' module")
        module_list = self.rpc.modules("web_selenium")

        if len(module_list) == 0:
            log.error("Can't locate 'web_selenium' module in database '{}'".format(db))
        else:
            if "web_selenium" in module_list.get("installed",[]):
                log.info("Module 'web_selenium' is installed")
            else:
                log.info("Trying to install module 'web_selenium'")
                self.rpc.install("web_selenium")
                log.info("Done")

    def close(self):
        """"
        Close any open resources
        """
        # driver
        self.driver.quit()
        # close xml-rpc, HOW ??

