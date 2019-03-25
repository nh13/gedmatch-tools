from typing import List

from gedmatch_tools.util import Kit
from gedmatch_tools.util import main_page
from gedmatch_tools.api._constants import KITS_XPATH
from gedmatch_tools.api._util import KIT_NAME_COLUMN, KIT_NUMBER_COLUMN
import lxml.html


def _ls() -> List[Kit]:
    '''Returns the the kits available on GEDMatch.com'''

    kits: List[Kit] = []

    driver = main_page()

    try:
        root = lxml.html.fromstring(driver.page_source)
        for row in root.xpath(KITS_XPATH + '//tr'):
            columns = row.xpath('.//td')

            # kit number
            number_col = columns[KIT_NUMBER_COLUMN]
            number = list(number_col.iterlinks())[0][0].text

            # kit name
            name_col = columns[KIT_NAME_COLUMN]
            name_col_links = list(name_col.iterlinks())
            if len(name_col_links) == 0:
                name = name_col.text
            else:
                name = name_col_links[0][0].text

            kit: Kit = Kit(name=name, number=number)
            kits.append(kit)
    except Exception as e:
        driver.close()
        raise e

    driver.close()

    return kits
