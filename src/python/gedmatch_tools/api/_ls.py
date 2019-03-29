from typing import List
from typing import Optional

import lxml.html
from selenium.webdriver.remote.webdriver import WebDriver

from gedmatch_tools.api._constants import KITS_XPATH
from gedmatch_tools.api._util import kit_from_lxml_row
from gedmatch_tools.util import Kit
from gedmatch_tools.util import KitStatus
from gedmatch_tools.util import main_page


def _ls(driver: Optional[WebDriver] = None, status: Optional[List[KitStatus]] = None) -> List[Kit]:
    '''Returns the the kits available on GEDMatch.com

    Args:
        status: return only kits with the given status(es)
    '''

    kits: List[Kit] = []

    _driver = main_page() if driver is None else driver

    try:
        root = lxml.html.fromstring(_driver.page_source)
        for row in root.xpath(KITS_XPATH + '//tr'):
            kit: Kit = kit_from_lxml_row(row)
            if status is None or kit.status in status:
                kits.append(kit)
    except Exception as e:
        _driver.close()
        raise e

    if driver is None:
        _driver.close()

    return kits
