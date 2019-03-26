import logging
from pathlib import Path
from typing import Dict, List, Optional

from gedmatch_tools.api import ls, one_to_many as one_to_many_api, OneToManyAutosomeResult
from gedmatch_tools.util import Kit


def one_to_many(*,
                kit: str,
                output: Path,
                max_matches: Optional[int] = None
                ) -> List[OneToManyAutosomeResult]:
    '''Performs one-to-many autosomal analysis.

    Args:
        kit: the name or number
        output: the output file.
        max_matches: the maximum # of matches to return
    Returns:
        A list of matches.
    '''
    return one_to_many_api(kit, output, max_matches=max_matches)


def one_to_many_tuples(*,
                       kits: List[str],
                       output_prefix: Path,
                       max_matches: Optional[int] = None
                       ) -> List[Optional[List[OneToManyAutosomeResult]]]:
    '''Performs one-to-many autosomal analysis.

    Args:
        kits: one or more kit names or numbers.
        output_prefix: the path prefix for the output files.
        max_matches: the maximum # of matches to return
    '''

    logging.info(f'retrieving list of kits.')
    kits_dict: Dict[str, Kit] = dict([(kit.number, kit) for kit in ls()])

    results: List[Optional[List[OneToManyAutosomeResult]]] = []
    logging.info(f'processing {len(kits)} kit pairs.')
    for i, kit in enumerate(kits, 1):
        logging.info(f'processing ({i}/{len(kits)}): {kit}.')
        output = Path(str(output_prefix) + f'{kit}.txt')
        result = one_to_many_api(kit=kit, output=output, max_matches=max_matches, kits=kits_dict)
        if result is None:
            logging.warning(f'No 1:1 autosomal match found for kit {kit}.')
        results.append(result)

    return results
