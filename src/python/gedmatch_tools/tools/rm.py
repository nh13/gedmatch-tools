import logging

from gedmatch_tools.api import rm as rm_api, rm_r as rm_r_api
from gedmatch_tools.tools import _query_yes_no


def rm(*number: str) -> None:
    '''Removes the kit(s) with the given number(s).

    Args:
        number: one or more numbers of kits to remove.
    '''

    rm_api(*number)


def rm_r(*, force: bool = False) -> None:
    '''Removes all kits on the GEDMatch website.
    *** WARNING *** this is potentially very destructive

    Args:
        force: true to not prompt for removal, false otherwise.
    '''

    if not force and not _query_yes_no("Are you sure you want to delete all kits?"):
        logging.info("Not deleting any kits.")
        return None

    rm_r_api()
