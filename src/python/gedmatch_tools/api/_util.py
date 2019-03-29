
from typing import Optional

from gedmatch_tools.util import Kit
from gedmatch_tools.util import KitStatus

KIT_NUMBER_COLUMN: int = 0
KIT_STATUS_COLUMN: int = 2
KIT_NAME_COLUMN: int = 3
KIT_EDIT_COLUMN: int = -1


def kit_from_lxml_row(row) -> Kit:  # type: ignore
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

    # kit status
    status_col = columns[KIT_STATUS_COLUMN]
    imgs = status_col.xpath('.//img')
    assert len(imgs) == 1
    src = imgs[0].attrib['src']
    status: Optional[KitStatus] = None
    for kit_status in KitStatus:
        if kit_status.value.src == src:
            status = kit_status
    assert status is not None, f'Could not parse src for status: {src}'

    kit: Kit = Kit(name=name, number=number, status=status)
    return kit


def kit_from_columns(columns) -> Kit:  # type: ignore
    '''Returns the kit for the given columns in the kit table from the main page.'''
    return Kit(name=columns[KIT_NAME_COLUMN].text, number=columns[KIT_NUMBER_COLUMN].text)
