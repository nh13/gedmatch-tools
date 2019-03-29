
from typing import Optional

from gedmatch_tools.util import Kit
from gedmatch_tools.util import KitStatus

KIT_NUMBER_COLUMN: int = 0
KIT_STATUS_COLUMN: int = 2
KIT_NAME_COLUMN: int = 3
KIT_EDIT_COLUMN: int = -1


def maybe_href(td) -> str:  # type: ignore
    '''Extract the text from a column, which is either a text or an an <a></a> element'''
    td_links = list(td.iterlinks())
    if len(td_links) == 0:
        return td.text
    else:
        assert len(td_links) == 1
        return td_links[0][0].text


def kit_from_lxml_row(row) -> Kit:  # type: ignore
    columns = row.xpath('.//td')

    # kit number
    number_col = columns[KIT_NUMBER_COLUMN]
    number = list(number_col.iterlinks())[0][0].text

    # kit name
    name = maybe_href(columns[KIT_NAME_COLUMN])

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
