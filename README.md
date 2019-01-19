[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/fulcrumgenomics/fgbio/blob/master/LICENSE)
[![Language](http://img.shields.io/badge/language-python-brightgreen.svg)](https://www.python.org/)
[![Documentation Status](https://readthedocs.org/projects/gedmatch-tools/badge/?version=latest)](http://gedmatch-tools.readthedocs.io/en/latest/?badge=latest)


gedmatch-tools
====

Tools and Python API for [GEDMatch Genesis](https://genesis.gedmatch.com).

## Installation

Python 3.6 or higher is required.

To clone the repository: `git clone https://github.com/nh13/gedmatch-tools.git`.

To install locally: `python setup.py install`.

The command line utility can be run with `gedmatch-tools`

## Command Line

To see a list of available tools, run `gedmatch-tools --help`.

For example, the tool to list all kits is `gedmatch-tools ls --help`

## Documentation

See the following [Documentation](https://gedmatch-tools.readthedocs.io/en/latest/).

Until online documentation is available, see [API in the source](https://github.com/nh13/gedmatch-tools/blob/master/src/python/gedmatch_tools/api/__init__.py).
Alternatively, you can build API documentation locally with:
```bash
cd docs
make
open _build/html/index.html
```

## GEDMatch.com Credentials

GEDMatch.com redentials can retrieved in two ways:

1. Create a CSV file in `~/.gedmatch` with the following contents:

```
email,<your-email>
password,<your-password>
```
2. Copy your email and password into the environment variables `GEDMATCH_EMAIL` and `GEDMATCH_PASSWORD` respectively.

## Items to be completed prior to an initial release

- [ ] remaining features
  - [ ] 1:many autosomal comparison analysis
  - [ ] add github issues for other applications/routes (user-requests?)
- [ ] documentation
  - [ ] module, class, and method docs
  - [ ] web-hosted tool and python API documentation (readthedocs.io)
- [ ] packaging and distribution
  - [ ] bioconda
  - [ ] pypi
- [ ] testing
  - [ ] set up travis-ci, including testing email/password for logging into the GEDMatch site
  - [ ] uni testing
    - [ ] parsing credentials (`.gedmatch` file, environment variables)
    - [ ] getting to the main page (`gedmatch_tools.util.main_page()`)
    - [ ] adding a kit or kits (`gedmatch_tools.tools.add_kit.*`)
    - [ ] listing already added/uploaded kits (`gedmatch_tools.tools.list_kits`)
    - [ ] delete kit or kits ( `gedmatch_tools.tools.delete_kits`)
    - [ ] perform one or more 1:1 autosomal analyses (`gedmatch_tools.tools.one_to_one_autosomal`)
