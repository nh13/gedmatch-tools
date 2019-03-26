
from gedmatch_tools.util import Kit

KIT_NUMBER_COLUMN: int = 0
KIT_NAME_COLUMN: int = 3
KIT_EDIT_COLUMN: int = -1


def kit_from_lxml_row(row) -> Kit:
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
    return kit


def kit_from_columns(columns) -> Kit:
    '''Returns the kit for the given columns in the kit table from the main page.'''
    return Kit(name=columns[KIT_NAME_COLUMN].text, number=columns[KIT_NUMBER_COLUMN].text)


def kit_from_row(row) -> Kit:
    '''Returns the kit for the given row in the kit table from the main page.'''
    columns = row.find_elements_by_tag_name('td')
    return kit_from_columns(columns)
