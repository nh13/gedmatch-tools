import logging
from pathlib import Path
from typing import Optional

from gedmatch_tools.api import add as add_api
from gedmatch_tools.util import RawDataType


def add(*, genotypes: Path,
        name: str,
        raw_data_type: Optional[RawDataType] = None,
        fam: Optional[Path] = None) -> None:
    '''Performs a generic upload of the given genotype.

    The sample information when given will be used to determine the sex of the donor, otherwise
    it will default to female.

    Args:
        genotypes: the path to the genotype file.
        name: the name of the donor.
        raw_data_type: optionally the raw data type to select.
        fam: optionally a PLINK sample information file; see the following link
             `https://www.cog-genomics.org/plink2/formats#fam`
    '''
    add_api(genotypes, name, raw_data_type, fam)


def add_all(*,
            in_manifest: Path,
            out_manifest: Path,
            fam: Optional[Path] = None,
            keep_going: bool = False) -> None:
    '''Performs a generic upload of one or more genotypes specified in a manifest file.

    The sample information when given will be used to determine the sex of the donor, otherwise
    it will default to female.

    The input manifest should be comma-separated with at least the following header and columns:
    1. `genotypes_path` - the path to the genotypes
    2. `name` - the name of the donor
    The output manifest will have a `number` column appended, containing the kit number for each
    sample.

    The following columns are optional but will be used if present:
    3. `raw_data_type` - optionally the raw data type to select.

    Args:
        in_manifest: the path to input manifest
        out_manifest: the path to the output manifest
        fam: optionally a PLINK sample information file; see the following link
             `https://www.cog-genomics.org/plink2/formats#fam`
    '''
    with open(in_manifest, 'r') as fh_in, open(out_manifest, 'w') as fh_out:
        header = fh_in.readline().rstrip('\r\n').split(',')
        assert 'genotypes_path' in header
        assert 'name' in header
        fh_out.write(','.join(header + ['number']) + '\n')
        fh_out.flush()
        for line in fh_in:
            fields = line.rstrip('\r\n').split(',')
            d = dict(zip(header, fields))
            name = d['name']
            genotypes_path = Path(d['genotypes_path'])
            logging.info(f'Uploading {name}: {genotypes_path}')
            kit = None
            try:
                raw_data_type: Optional[RawDataType] = None
                if 'raw_data_type' in header:
                    raw_data_type = RawDataType.from_name(name=d['raw_data_type'])
                kit = add_api(genotypes_path, name, raw_data_type, fam)
            except Exception as e:
                if not keep_going:
                    logging.warning(f'Upload failed {name}: {genotypes_path}')
                    raise e
                else:
                    logging.exception(f'Upload failed {name}: {genotypes_path}')
            if kit is None:
                fields = fields + ['failed']
            else:
                logging.info(f'Kit number: {kit.number}')
                fields = fields + [kit.number]
            fh_out.write(','.join(fields) + '\n')
            fh_out.flush()
