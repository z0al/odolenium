#! python3
# -*- coding: utf-8 -*-
import contextlib

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of


@contextlib.contextmanager
def for_page_load(browser, timeout=30):
    """
    Wait for page load

    Credit
    ------
    @Tommy Beadle
    http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html#comment-1998325550
    """
    old_page = browser.find_element_by_tag_name('html')
    yield
    WebDriverWait(browser, timeout).until(staleness_of(old_page))
