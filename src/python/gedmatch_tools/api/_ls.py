from typing import List

from gedmatch_tools.util import Kit
from gedmatch_tools.util import main_page
from gedmatch_tools.api._constants import KITS_XPATH
from gedmatch_tools.api._util import kit_from_lxml_row
import lxml.html


def _ls() -> List[Kit]:
    '''Returns the the kits available on GEDMatch.com'''

    kits: List[Kit] = []

    driver = main_page()

    try:
        root = lxml.html.fromstring(driver.page_source)
        for row in root.xpath(KITS_XPATH + '//tr'):
            kit: Kit = kit_from_lxml_row(row)
            kits.append(kit)
    except Exception as e:
        driver.close()
        raise e

    driver.close()

    return kits
