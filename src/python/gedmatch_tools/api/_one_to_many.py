import logging
from pathlib import Path
from typing import Dict, List
from typing import Optional

import attr
import lxml.html
from selenium.webdriver.remote.webdriver import WebDriver

from gedmatch_tools.api._ls import _ls
from gedmatch_tools.util import Kit
from gedmatch_tools.util import main_page
from gedmatch_tools.util.metric import write_metrics


def _one_to_many(kit: str,
                 output: Path,
                 max_matches: Optional[int],
                 kits: Optional[Dict[str, Kit]] = None,
                 driver: Optional[WebDriver] = None
                 ) -> List['OneToManyAutosomeResult']:
    '''Performs one-to-many autosomal analysis.

    Args:
        kit: the name or number
        output: the output file.
        max_matches: the maximum # of matches to return
        kits: a mapping of kit name to kit, useful when performing many 1:1 analyses.

    Returns:
        A list of matches.
    '''
    results: List['OneToManyAutosomeResult'] = []

    _driver = main_page() if driver is None else driver

    if kits is None:
        kits = dict([(kit.number, kit) for kit in _ls(_driver)])

    if kit not in kits:
        kit = [n for n, k in kits.items() if k.name == kit][0]

    try:
        url = f'OneToMany0Tier2.php?kit_num={kit}'
        page = _driver.find_element_by_xpath('//a[@href="' + url + '"]')
        page.click()

        root = lxml.html.fromstring(_driver.page_source)
        for table in root.xpath("//table"):
            rows = [row for row in table.xpath('.//tr')]

            # check that the first column in the first row has value "Chr"
            tds = rows[0].xpath('.//td')
            first_column_value = tds[0].text
            if first_column_value != 'Kit':
                continue
            header = [td.text for td in tds]
            assert len(header) == 10, f'header: {header}'

            last_row: int = len(rows) if max_matches is None else max_matches + 1
            logging.info(f'Reading rows for {kit}')
            for row_num, row in enumerate(rows[1:last_row], 1):
                columns = [td.text for td in row.xpath('.//td')]
                assert len(columns) == 10, f'columns: {columns}'
                d = dict(zip(header, columns))

                result = OneToManyAutosomeResult(
                    kit_one=kits[kit],
                    kit_two=Kit(name=d['Name'], number=d['Kit'], email=d['Email'],
                                testing_company=d['Testing Company']),
                    largest_segment=float(d['Largest Seg']),
                    total_half_match_segments=float(d['Total cM']),
                    most_recent_common_ancestor=float(d['Gen']),
                    num_snps=int(d['Overlap']),
                    date_compared=d['Date Compared']
                )
                results.append(result)
            logging.info(f'Returning {len(results)} results.')
    except Exception as e:
        _driver.close()
        raise e

    if driver is None:
        _driver.close()

    write_metrics(output, results)

    return results


@attr.s(frozen=True)
class OneToManyAutosomeResult(object):
    '''The result of a one-to-one autosomal analysis.

    Attributes:
        kit_one: the kit for the first sample.
        kit_two: the kit for the second sample.
        largeset_segment: the size of the largest segment in centimorgans.
        total_half_match_segments: the total length of half-match segments in centimorgans.
        most_recent_common_ancestor: the # of generations until the most recent common ancestor.
        num_snps: the number of SNPs used in this analysis.
        date_compared: the date the kit was compared
    '''

    kit_one: Kit = attr.ib()
    kit_two: Kit = attr.ib()
    largest_segment: float = attr.ib()
    total_half_match_segments: float = attr.ib()
    most_recent_common_ancestor: float = attr.ib()
    num_snps: int = attr.ib()
    date_compared: str = attr.ib()
