#! python3
# -*- coding: utf-8 -*-
import contextlib

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions
from selenium.common.exceptions import NoSuchElementException

from erppeek import Client, Error

from .util import *
from .error import *
from .conf import *
from . import wait

# Supported Odoo server versions
versions = ['9.0c']

class OdooUI(object):

    def __init__(self, driver, config):
        self.driver = driver
        self.setup(config)

        self.url = parse_url(self.config['url'])

        if self.url is None:
            raise OdoleniumError("'{}' isn't valid URL".format(self.config['url']))

        log.info('Setting up XML-RPC connection to {}'.format(self.urlgen()))
        try:
            self.rpc = Client(self.url.geturl())
            log.info('Connection succeed')
        except:
            log.error("Connection failed")
            raise ConnectionRefusedError("Can't connect to Odoo server")

        self.ver = self.rpc.db.server_version()
        log.info("Found version {} Odoo server".format(self.ver))

        if self.ver not in versions:
            raise OdoleniumError("Unsupported Odoo version '{}'".format(self.ver))

    def login(self, user, password, db):
        """
        Login to Odoo server using given user and password and
        (optionaly) database.
        """
        log.info('Trying to log in over XML-RPC')
        # setup rpc login
        try:
            self.rpc.login(user,password,db)
        except Error as er: # erppeek.Error
            raise OdoleniumError("{}".format(er))

        log.info("Logged in as '{}'".format(self.rpc.user))

        log.info("Searching for 'web_selenium' module")
        module_list = self.rpc.modules('web_selenium')

        if len(module_list) == 0:
            log.error("Can't locate 'web_selenium' module in database '{}'".format(db))
        else:
            if 'web_selenium' in module_list.get('installed',[]):
                log.info("module 'web_selenium' is installed")
            else:
                log.info("tying to install module 'web_selenium'")
                self.rpc.install('web_selenium')
                log.info('done')

        log.info('GET {}'.format(self.url.geturl()))
        self.driver.get(self.url.geturl())
        # v9.0c
        if self.ver == '9.0c':
            cur = parse_url(self.driver.current_url)

            # db urls
            url_rgx = ['/database/selector','/database/manager']

            if any(u in cur.path for u in url_rgx):

                db_list = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    '.o_database_list .list-group .list-group-item'
                )

                for d in db_list:
                    if d.text == db:
                        db = d

                # select db
                db.click()

            # fill in login form.
            login_field = self.driver.find_element(By.ID, u'login')
            login_field.send_keys(user)
            password_field = self.driver.find_element(By.ID, u'password')
            password_field.send_keys(password)
            login_button = self.driver.find_element(
                By.CSS_SELECTOR,
                ".btn.btn-primary[type='submit']"
            )
            with self.wait_for_page_load():
                login_button.click()

    def setup(self,config):
        self.config = loadconfig(config)

    def urlgen(self, path=""):
        """
        Generate URL.
        """
        base = '://'.join([self.url.scheme, self.url.netloc+'/'])
        return u'{base:s}/{path:s}'.format(
            base=base,
            path=path.lstrip('/'),
        )

    @contextlib.contextmanager
    def wait_for_page_load(self):
        """
        Wait for full page load and assert new page has been loaded.

        Credit
        -------
        benoitbryon at https://github.com/meta-it/odooselenium/blob/develop/odooselenium/ui.py#L39
        """
        # Inspect initial state.
        try:
            initial_body = self.driver.find_element(By.XPATH, '//body')
        except NoSuchElementException:  # First load.
            initial_body = None

        # Yield (back to 'with' block, where user triggers page load).
        yield

        # Wait for body to change.
        ui.WebDriverWait(self.driver, 10).until(
            expected_conditions.staleness_of(initial_body)
        )
