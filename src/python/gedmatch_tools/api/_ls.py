from typing import List

from gedmatch_tools.util import Kit
from gedmatch_tools.util import main_page
from gedmatch_tools.api._constants import KITS_XPATH
from gedmatch_tools.api._util import kit_from_row


def _ls() -> List[Kit]:
    '''Returns the the kits available on GEDMatch.com'''

    kits: List[Kit] = []

    driver = main_page()

    try:
        kits_table = driver.find_element_by_xpath(KITS_XPATH)
        for row in kits_table.find_elements_by_tag_name('tr'):
            kit: Kit = kit_from_row(row)
            kits.append(kit)
    except Exception as e:
        driver.close()
        raise e

    driver.close()

    return kits
