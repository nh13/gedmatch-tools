from pathlib import Path
from typing import Dict, List, Optional

from gedmatch_tools.api._add import _add
from gedmatch_tools.api._ls import _ls
from gedmatch_tools.api._one_to_one import _one_to_one, OneToOneAutosomeResult
from gedmatch_tools.api._one_to_one import SegmentResult  # noqa: F401
from gedmatch_tools.api._rm import _rm
from gedmatch_tools.util import Kit


def one_to_one(kit_one: str,
               kit_two: str,
               output_prefix: Path,
               kits: Optional[Dict[str, Kit]] = None
               ) -> Optional[OneToOneAutosomeResult]:
    '''Performs one-to-one autosomal analysis.

    Args:
        kit_one: the first kit name or number
        kit_two: the second kit name or number
        output_prefix: the prefix for the output files.
        kits: a mapping of kit name to kit, useful when performing many 1:1 analyses.

    Returns:
        None if the analysis did not find any segments, otherwise the analysis results.
    '''
    return _one_to_one(kit_one, kit_two, output_prefix, kits)


def add(genotypes: Path, name: str, fam: Optional[Path] = None) -> Kit:
    '''Performs a generic upload of the given genotype.

    The sample information when given will be used to determine the sex of the donor, otherwise
    it will default to female.

    Args:
        genotypes: the path to the genotype file.
        name: the name of the donor.
        fam: optionally a PLINK sample information file; see the following link
             https://www.cog-genomics.org/plink2/formats#fam

    Returns:
        the kit created by GEDMatch

    Raises:
        Exception: if the kit could not be uploaded
    '''
    return _add(genotypes, name, fam)


def ls() -> List[Kit]:
    '''Returns the the kits available on GEDMatch.com'''
    return _ls()


def rm(*number: str) -> None:
    '''Removes the kit(s) with the given number(s).'''
    for n in number:
        _rm(n)


def rm_r() -> None:
    '''Removes all kits on the GEDMatch website.'''
    rm(*ls())
