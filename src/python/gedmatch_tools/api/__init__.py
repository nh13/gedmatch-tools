from pathlib import Path
from typing import Dict, List, Optional

from gedmatch_tools.api._add import _add
from gedmatch_tools.api._ls import _ls
from gedmatch_tools.api._one_to_many import OneToManyAutosomeResult  # noqa: F401
from gedmatch_tools.api._one_to_many import _one_to_many
from gedmatch_tools.api._one_to_one import SegmentResult  # noqa: F401
from gedmatch_tools.api._one_to_one import _one_to_one, OneToOneAutosomeResult
from gedmatch_tools.api._rm import _rm_impl
from gedmatch_tools.util import Credentials
from gedmatch_tools.util import Kit, RawDataType
from gedmatch_tools.util import main_page
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver


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


def one_to_many(kit: str,
                output: Path,
                max_matches: Optional[int],
                kits: Optional[Dict[str, Kit]] = None,
                driver: Optional[WebDriver] = None) -> \
        List[OneToManyAutosomeResult]:
    '''Performs one-to-many autosomal analysis.

    Args:
        kit: the name or number
        output: the output file.
        max_matches: the maximum # of matches to return
        kits: a mapping of kit name to kit, useful when performing many 1:1 analyses.

    Returns:
        A list of matches.
    '''
    return _one_to_many(kit, output, max_matches, kits, driver)


def add(genotypes: Path,
        name: str,
        raw_data_type: Optional[RawDataType] = None,
        fam: Optional[Path] = None) -> Kit:
    '''Performs a generic upload of the given genotype.

    The sample information when given will be used to determine the sex of the donor, otherwise
    it will default to female.

    Args:
        genotypes: the path to the genotype file.
        name: the name of the donor.
        raw_data_type: optionally the raw data type to select.
        fam: optionally a PLINK sample information file; see the following link
             https://www.cog-genomics.org/plink2/formats#fam

    Returns:
        the kit created by GEDMatch

    Raises:
        Exception: if the kit could not be uploaded
    '''
    return _add(genotypes, name, raw_data_type, fam)


def ls(driver: Optional[WebDriver] = None) -> List[Kit]:
    '''Returns the the kits available on GEDMatch.com'''
    return _ls(driver)


def rm(*number: str) -> None:
    '''Removes the kit(s) with the given number(s).'''

    credentials = Credentials.build()
    driver = main_page()
    last_time = datetime.now()
    for n in number:
        # Re-login if it takes too long
        if (datetime.now() - last_time).total_seconds() > 30:
            driver.close()
            driver = main_page()
        last_time = datetime.now()
        _rm_impl(number=n, credentials=credentials, driver=driver)

    driver.close()


def rm_r() -> None:
    '''Removes all kits on the GEDMatch website.'''
    rm(*ls())  # type: ignore
