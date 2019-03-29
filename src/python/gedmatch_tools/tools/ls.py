from typing import List

from gedmatch_tools.api import ls as ls_api
from gedmatch_tools.util import KitStatus


def ls(*, status: List[KitStatus] = []) -> None:
    '''Lists the kits available on GEDMatch.com

    Args:
        status: return only kits with the given status(es)
    '''
    _status = None if len(status) == 0 else status
    print('kit_name\tkit_number')
    for kit in ls_api(status=_status):
        print(f'{kit.name}\t{kit.number}')
