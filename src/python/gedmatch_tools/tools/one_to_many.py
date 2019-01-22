from pathlib import Path
from typing import List, Optional

from gedmatch_tools.api import one_to_many as one_to_many_api, OneToManyAutosomeResult


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