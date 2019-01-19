'''Provides some default methods for the :py:mod:`~selenium` module.'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


def default_webdriver() -> WebDriver:
    '''Returns a default headless webddriver.'''
    opts = Options()
    opts.set_headless()
    assert opts.headless  # operating in headless mode
    return webdriver.Firefox(options=opts)
