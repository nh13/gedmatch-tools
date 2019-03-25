import logging

from gedmatch_tools.util import Credentials
from gedmatch_tools.util import main_page
from gedmatch_tools.api._constants import KITS_XPATH
from gedmatch_tools.api._util import kit_from_columns


def _rm(number: str) -> None:
    '''Removes the kit with the given number.'''
    credentials = Credentials.build()

    driver = main_page()

    try:
        kits_table = driver.find_element_by_xpath(KITS_XPATH)
        found_kit = False
        for row in kits_table.find_elements_by_tag_name('tr'):
            columns = row.find_elements_by_tag_name('td')
            kit: Kit = kit_from_columns(columns)
            if kit.number != number:
                continue
            elem = columns[-1].find_element_by_css_selector(
                "form[action='KitProfile.php']"
            )
            elem.click()
            found_kit = True
            break

        if not found_kit:
            raise Exception(f'Could not find kit {kit.number} to delete.')

        tab = driver.find_element_by_css_selector("a[href='#2a']")
        tab.click()

        password = driver.find_element_by_css_selector(
            "input[type='PASSWORD'][name='VerifyPassword']")
        password.send_keys(credentials.password)

        submit = driver.find_element_by_css_selector(
            "input[type='SUBMIT'][value='Delete']")
        submit.click()

        # are you sure?
        alert_one = driver.switch_to.alert
        alert_one.accept()
        driver.switch_to.parent_frame()

        logging.info(f'Deleted kit: {number}')

    except Exception as e:
        print(driver.page_source)
        driver.close()
        raise e

    driver.close()
