from pathlib import Path
from typing import Dict, List, Optional

import attr

from gedmatch_tools.api._ls import _ls
from gedmatch_tools.util import Kit
from gedmatch_tools.util import main_page
from gedmatch_tools.util.metric import write_metric, write_metrics


def _comma_value_to_int(value: str) -> int:
    '''Converts a comma separated number (ex. 123,456) to an integer.'''
    return int(value.replace(',', ''))


def _one_to_one(kit_one: str,
                kit_two: str,
                output_prefix: Path,
                kits: Optional[Dict[str, Kit]] = None
                ) -> Optional['OneToOneAutosomeResult']:
    '''Performs one-to-one autosomal analysis.

    Args:
        kit_one: the first kit name or number
        kit_two: the second kit name or number
        output_prefix: the prefix for the output files.
        kits: a mapping of kit name to kit, useful when performing many 1:1 analyses.

    Returns:
        None if the analysis did not find any segments, otherwise the analysis results.
    '''
    if kits is None:
        kits = dict([(kit.number, kit) for kit in _ls()])

    if kit_one not in kits:
        kit_one = [n for n, k in kits.items() if k.name == kit_one][0]
    if kit_two not in kits:
        kit_two = [n for n, k in kits.items() if k.name == kit_two][0]

    driver = main_page()

    try:
        url = 'v_compare1.php'
        page = driver.find_element_by_xpath('//a[@href="' + url + '"]')
        page.click()

        kit1 = driver.find_element_by_name('kit1')
        kit1.clear()
        kit1.send_keys(kit_one)

        kit2 = driver.find_element_by_name('kit2')
        kit2.clear()
        kit2.send_keys(kit_two)

        submit = driver.find_element_by_name('xsubmit')
        submit.click()

        segments: List[SegmentResult] = []
        for table in driver.find_elements_by_xpath('//table'):
            rows = table.find_elements_by_tag_name('tr')

            # check that the first column in the first row has value "Chr"
            first_column_value = rows[0].find_elements_by_tag_name('td')[0].text
            if first_column_value != 'Chr':
                continue

            for row in rows[1:]:
                columns = row.find_elements_by_tag_name('td')
                assert len(columns) == 5

                segment = SegmentResult(
                    chromosome=columns[0].text,
                    start=_comma_value_to_int(columns[1].text),
                    end=_comma_value_to_int(columns[2].text),
                    centimorgans=float(columns[3].text),
                    num_snps=_comma_value_to_int(columns[4].text)
                )
                segments.append(segment)

        largest_segment: float = 0.0
        total_half_match_segments: float = 0.0
        pct_half_match_segments: float = 0.0
        most_recent_common_ancestor: float = -1.0
        shared_segments: int = 0
        num_snps: int = 0
        pct_snps_identical: float = 0.0
        version: str = 'none found'

        for line in driver.page_source.split('\n'):
            line = line.rstrip('\r\n').strip()
            line = line.replace('<br>', '')

            if 'No shared DNA segments found' in line:
                assert len(segments) == 0
            elif 'Largest segment' in line:
                largest_segment = float(line.split(' = ')[1].split(' ')[0])
            elif 'Total Half-Match segments' in line:
                fields = line.split(' = ')[1].split(' ')
                total_half_match_segments = float(fields[0])
                pct_half_match_segments = float(fields[2].replace('(', '').replace(')', ''))
            elif 'Estimated number of generations to MRCA' in line:
                most_recent_common_ancestor = float(line.split(' = ')[1].split(' ')[0])
            elif 'shared segments found for this comparison' in line:
                shared_segments = int(line.split(' ')[0])
            elif 'SNPs used for this comparison' in line:
                num_snps = int(line.split(' ')[0])
            elif 'Pct SNPs are full identical' in line:
                pct_snps_identical = float(line.split(' ')[0])
            elif 'Ver:' in line:
                version = line.replace('<font size="2">Ver: ', '') \
                    .replace('</font>', '') \
                    .replace(' ', '-')

        final_result = None
        vars = [largest_segment, total_half_match_segments, pct_half_match_segments,
                most_recent_common_ancestor, shared_segments, num_snps, pct_snps_identical,
                version]
        if all([v is not None for v in vars]):
            final_result = OneToOneAutosomeResult(
                kit_one=kits[kit_one],
                kit_two=kits[kit_two],
                segments=segments,
                largest_segment=largest_segment,
                total_half_match_segments=total_half_match_segments,
                pct_half_match_segments=pct_half_match_segments,
                most_recent_common_ancestor=most_recent_common_ancestor,
                shared_segments=shared_segments,
                num_snps=num_snps,
                pct_snps_identical=pct_snps_identical,
                version=version
            )

    except Exception as e:
        driver.close()
        raise e

    driver.close()

    if final_result is not None:
        summary: Path = Path(str(output_prefix) + '.summary.txt')
        write_metric(summary, final_result)
        detailed: Path = Path(str(output_prefix) + '.detailed.txt')
        write_metrics(detailed, final_result.segments)

    return final_result


@attr.s(frozen=True)
class SegmentResult(object):
    '''A single segment result.

    Attributes:
        chromosome: the chromosome of the segment
        start: the 1-based start position of the segment
        end: the 1-based end position (inclusive) of the segment
        centimorgans: the genetic distance in centimorgans of the segment
        num_snps: the number of snps within this segment.
    '''

    chromosome: str = attr.ib()
    start: int = attr.ib()
    end: int = attr.ib()
    centimorgans: float = attr.ib()
    num_snps: int = attr.ib()


@attr.s(frozen=True)
class OneToOneAutosomeResult(object):
    '''The result of a one-to-one autosomal analysis.

    Attributes:
        kit_one: the kit for the first sample.
        kit_two: the kit for the second sample.
        segments: the segments found, if any.
        largeset_segment: the size of the largest segment in centimorgans.
        total_half_match_segments: the total length of half-match segments in centimorgans.
        pct_half_match_segments: the percentage of half-match segments.
        most_recent_common_ancestor: the # of generations until the most recent common ancestor.
        shared_segments: the number of shared segments.
        num_snps: the number of SNPs used in this analysis.
        pct_snps_identical: the percentage of SNPs that were identical
        version: str = the version of analysis.
    '''

    kit_one: Kit = attr.ib()
    kit_two: Kit = attr.ib()
    segments: List[SegmentResult] = attr.ib(metadata={'print': False})
    largest_segment: float = attr.ib()
    total_half_match_segments: float = attr.ib()
    pct_half_match_segments: float = attr.ib()
    most_recent_common_ancestor: float = attr.ib()
    shared_segments: int = attr.ib()
    num_snps: int = attr.ib()
    pct_snps_identical: float = attr.ib()
    version: str = attr.ib()
