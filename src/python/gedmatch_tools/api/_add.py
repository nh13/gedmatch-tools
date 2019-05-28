from pathlib import Path
from typing import Dict, Optional

import attr
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait

from gedmatch_tools.util import Kit, RawDataType
from gedmatch_tools.util import main_page


def _add(genotypes: Path,
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
    kit_number: str = ''

    fam_dict = _read_fam(fam) if fam is not None else {}

    driver = main_page()

    try:
        url = 'v_upload1.phpnf'
        page = driver.find_element_by_xpath('//a[@href="' + url + '"]')
        page.click()

        in_name = driver.find_element_by_name('name')
        in_name.clear()
        in_name.send_keys(name)

        male = False if name not in fam_dict or not fam_dict[name].sex else True
        if male:
            in_male = driver.find_element_by_css_selector(
                "input[type='radio'][value='M'][name='sex']")
            in_male.click()
        else:
            in_female = driver.find_element_by_css_selector(
                "input[type='radio'][value='F'][name='sex']")
            in_female.click()

        in_source = Select(driver.find_element_by_name('source'))
        in_source.select_by_index(21)  # other

        raw_data_type_value = str(6 if raw_data_type is None else raw_data_type.value)
        in_auth = driver.find_element_by_css_selector(
            "input[type='radio'][value='" + raw_data_type_value + "'][name='auth']")
        in_auth.click()

        in_public = driver.find_element_by_css_selector(
            "input[type='radio'][value='Y'][name='public2']"
        )
        in_public.click()

        in_file = driver.find_element_by_css_selector(
            "input[type='file'][name='GedcomFile']")
        in_file.send_keys(str(genotypes.resolve()))

        submit = driver.find_element_by_css_selector(
            "input[type='submit'][name='gedsubmit']")
        submit.click()

        wait_for_link_text = 'Click here to get to Home'
        WebDriverWait(driver, 90).until(
            expected_conditions.visibility_of_element_located(
                (By.LINK_TEXT, wait_for_link_text)))

        for line in driver.page_source.split('\n'):
            if 'Assigned kit number:' in line:
                line = line.rstrip('\r\n').strip().replace('</font>', '')
                kit_number = line.split('>')[-1]
                break
        else:
            raise ValueError('No kit number returned by GEDmatch.')

    except Exception as e:
        print(driver.page_source)
        driver.close()
        raise e

    driver.close()

    return Kit(name=name, number=kit_number)


@attr.s
class _SampleInfo(object):
    '''Sample information'''

    family_id: str = attr.ib()
    sample_id: str = attr.ib()
    father_id: str = attr.ib()
    mother_id: str = attr.ib()
    sex: Optional[bool] = attr.ib()
    phenotype: str = attr.ib()


def _read_fam(fam: Path) -> Dict[str, _SampleInfo]:
    '''Reads a PLINK FAM file.

    Args:
        fam: the path to the FAM file.

    Returns:
        a dictionary of sample ids to sample information
    '''
    d: Dict[str, _SampleInfo] = dict()
    with open(fam, 'r') as fh:
        for line in fh:
            fields = line.rstrip('\r\n').split(' ')

            d[fields[1]] = _SampleInfo(
                family_id=fields[0],
                sample_id=fields[1],
                father_id=fields[2],
                mother_id=fields[3],
                sex=fields[4] == '1',
                phenotype=fields[5]
            )

    return d
