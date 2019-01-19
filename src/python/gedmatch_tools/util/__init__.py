'''Useful utility methods.'''

import os
from pathlib import Path
from typing import Optional

import attr
from selenium.webdriver.remote.webdriver import WebDriver

from gedmatch_tools.util.selenium_util import default_webdriver
from gedmatch_tools.util.settings import genesis_login_url


def main_page() -> WebDriver:
    '''Logs into the GEDMatch genesis site and moves to the main-page.

    Returns:
        a web-driver logged in and at the main GEDMatch genesis page.
    '''

    credentials = Credentials.build()
    driver = default_webdriver()

    try:
        # login
        driver.get(genesis_login_url)

        email_element = driver.find_element_by_name('email')
        email_element.clear()
        email_element.send_keys(credentials.email)

        password_element = driver.find_element_by_name("password")
        password_element.clear()
        password_element.send_keys(credentials.password)

        login_element = driver.find_element_by_xpath(
            '/html/body/center/table/tbody/tr[3]/td/form/table/tbody/tr[4]/td[2]/input')
        login_element.click()

    except Exception as e:
        driver.close()
        raise e

    return driver


@attr.s(frozen=True)
class Kit(object):
    '''Class for storing information about a GEDMatch kit.

    Attributes:
        name: the name of the kit (assigned during import)
        number: the number of the kit (assigned by GEDMatch)
    '''

    name: str = attr.ib()
    number: str = attr.ib()


@attr.s(frozen=True)
class Credentials(object):
    '''Class for storing GEDMatch credentials.

    Attributes:
        email: the login email
        password: the login password
    '''

    email: str = attr.ib()
    password: str = attr.ib()

    @classmethod
    def build(cls, config_path: Optional[Path] = None) -> 'Credentials':
        '''Builds a set of credentials.

        First, the config path will be read to find the credentials.  If no config file is present,
        the GEDMATCH_EMAIL and GEDMATCH_PASSWORD environment variables are used.

        Args:
            config_path: optionally the path to the config file.

        '''
        email: str = ''
        password: str = ''
        if config_path is None:
            config_path = Path.home() / '.gedmatch'
        if config_path.exists():
            with open(config_path, 'r') as fh:
                for line in fh:
                    line = line.rstrip('\r\n')
                    fields = line.split(',', 1)
                    assert len(fields) == 2, f'Invalid config line: {line}'
                    if fields[0] == 'email':
                        email = fields[1]
                    elif fields[0] == 'password':
                        password = fields[1]
                    else:
                        raise Exception(f'Unknown field: {fields[0]}')
        else:
            email = os.environ['GEDMATCH_EMAIL']
            password = os.environ['GEDMATCH_PASSWORD']
        return Credentials(email=email, password=password)
