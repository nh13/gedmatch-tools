import logging

from gedmatch_tools.util import Credentials
from gedmatch_tools.util import main_page


def _rm(number: str) -> None:
    '''Removes the kit with the given number.'''
    credentials = Credentials.build()

    driver = main_page()

    try:
        kits_xpath = '/html/body/center/table/tbody/tr[2]/td/center/table[1]/tbody/tr/td[1]/' + \
            'table/tbody/tr[4]/td/table/tbody/tr[3]/td/table'
        kits_table = driver.find_element_by_xpath(kits_xpath)
        for row in kits_table.find_elements_by_tag_name('tr'):
            columns = row.find_elements_by_tag_name('td')
            if columns[0].text != number:
                continue
            elem = columns[3].find_element_by_css_selector(
                "form[action='KitProfile.php']"
            )
            elem.click()
            break

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
