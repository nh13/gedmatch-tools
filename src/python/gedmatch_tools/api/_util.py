
from gedmatch_tools.util import Kit

KIT_NUMBER_COLUMN: int = 0
KIT_NAME_COLUMN: int = 3
KIT_EDIT_COLUMN: int = -1


def kit_from_columns(columns) -> Kit:
    '''Returns the kit for the given columns in the kit table from the main page.'''
    return Kit(name=columns[KIT_NAME_COLUMN].text, number=columns[KIT_NUMBER_COLUMN].text)


def kit_from_row(row) -> Kit:
    '''Returns the kit for the given row in the kit table from the main page.'''
    columns = row.find_elements_by_tag_name('td')
    return kit_from_columns(columns)
