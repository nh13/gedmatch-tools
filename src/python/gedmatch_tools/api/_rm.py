import logging

import lxml.html
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from gedmatch_tools.api._constants import HOME_PAGE_XPATH
from gedmatch_tools.api._constants import KITS_XPATH
from gedmatch_tools.api._util import kit_from_columns, kit_from_lxml_row
from gedmatch_tools.util import Credentials
from gedmatch_tools.util import main_page
from gedmatch_tools.util.settings import genesis_home_page_url
from gedmatch_tools.util import Kit


def _rm_impl(number: str, credentials: Credentials, driver: WebDriver) -> None:
    '''Removes the kit with the given number.'''

    try:
        # First try to find the row quickly
        root = lxml.html.fromstring(driver.page_source)
        row_index = -1
        for idx, row in enumerate(root.xpath(KITS_XPATH + '//tr')):
            kit: Kit = kit_from_lxml_row(row)
            if kit.number == number:
                row_index = idx
                break

        if row_index < 0:
            raise Exception(f'Could not find kit {number} to delete.')

        # Click on the edit/pencil button
        kits_table = driver.find_element_by_xpath(KITS_XPATH)
        row = kits_table.find_elements_by_tag_name('tr')[row_index]
        columns = row.find_elements_by_tag_name('td')
        kit = kit_from_columns(columns)
        assert kit.number == number
        elem = columns[-1].find_element_by_css_selector("form[action='KitProfile.php']")
        elem.click()

        tab = driver.find_element_by_css_selector("a[href='#2a']")
        tab.click()

        password = driver.find_element_by_css_selector(
            "input[type='PASSWORD'][name='VerifyPassword']")
        password.send_keys(credentials.password)

        submit = driver.find_element_by_css_selector(
            "input[type='SUBMIT'][value='Delete']")
        submit.click()

        # are you sure?
        alert = driver.switch_to.alert
        alert.accept()
        driver.switch_to.parent_frame()

        # kit was deleted, ok?
        WebDriverWait(driver, 90).until(
            expected_conditions.alert_is_present(),
            'Kit deletion confirmation was not detected'
        )
        alert = driver.switch_to.alert
        alert.accept()
        driver.switch_to.parent_frame()
        logging.info(f'Deleted kit: {number}')

        # wait to go to the home page
        WebDriverWait(driver, 90).until(
            expected_conditions.url_to_be(genesis_home_page_url),
            'Did not return to the home page'
        )
        WebDriverWait(driver, 90).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, HOME_PAGE_XPATH)
            )
        )
    except Exception as e:
        print(driver.page_source)
        driver.close()
        raise e


def _rm(number: str) -> None:
    '''Removes the kit with the given number.'''
    credentials = Credentials.build()
    driver = main_page()
    _rm_impl(number=number, credentials=credentials, driver=driver)
    driver.close()
