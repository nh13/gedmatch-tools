import logging
from pathlib import Path
from typing import Dict, List, Optional

from gedmatch_tools.api import ls, one_to_one as one_to_one_api, OneToOneAutosomeResult
from gedmatch_tools.util import Kit
from gedmatch_tools.util.metric import write_metrics


def one_to_one(*,
               kit_one: str,
               kit_two: str,
               output_prefix: Path) -> Optional[OneToOneAutosomeResult]:
    '''Performs one-to-one autosomal analysis.

    Args:
        kit_one: the name or number of the first kit
        kit_two: the name or number of the second kit
        output_prefix: the path prefix for the output files.
    '''
    return one_to_one_api(kit_one, kit_two, output_prefix)


def one_to_one_tuples(*,
                      kits: List[str],
                      output_prefix: Path
                      ) -> List[Optional[OneToOneAutosomeResult]]:
    '''Performs one-to-one autosomal analysis.

    Args:
        kits: one or more kit name or number tuples (comma seperated).
        output_prefix: the path prefix for the output files.
    '''

    logging.info(f'retrieving list of kits.')
    kits_dict: Dict[str, Kit] = dict([(kit.number, kit) for kit in ls()])

    results: List[Optional[OneToOneAutosomeResult]] = []
    logging.info(f'processing {len(kits)} kit pairs.')
    for i, kit_tuple in enumerate(kits, 1):
        kit_one, kit_two = kit_tuple.split(',')
        logging.info(f'processing ({i}/{len(kits)}) kits {kit_one} and {kit_two}.')
        tuple_output_prefix = Path(str(output_prefix) + f'.{kit_one}-{kit_two}')
        result = one_to_one_api(kit_one=kit_one,
                                kit_two=kit_two,
                                output_prefix=tuple_output_prefix,
                                kits=kits_dict)
        if result is None:
            logging.warning(f'No 1:1 autosomal match found for kits {kit_one} and {kit_two}.')
        results.append(result)

    logging.info(f'writing output.')
    summary: Path = Path(str(output_prefix) + '.summary.txt')
    write_metrics(summary, results)

    return results
