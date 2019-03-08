from typing import List

from gedmatch_tools.util import Kit
from gedmatch_tools.util import main_page


def _ls() -> List[Kit]:
    '''Returns the the kits available on GEDMatch.com'''

    kits: List[Kit] = []

    driver = main_page()

    try:
        kits_xpath = '/html/body/center/table/tbody/tr[2]/td/center/table[1]/tbody/tr/td[1]' + \
                     '/table/tbody/tr[4]/td/table/tbody/tr[4]/td/table'
        kits_table = driver.find_element_by_xpath(kits_xpath)
        for row in kits_table.find_elements_by_tag_name('tr'):
            columns = row.find_elements_by_tag_name('td')
            kit = Kit(name=columns[1].text, number=columns[0].text)
            kits.append(kit)
    except Exception as e:
        driver.close()
        raise e

    driver.close()

    return kits
