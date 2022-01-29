[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/fulcrumgenomics/fgbio/blob/master/LICENSE)
[![Language](http://img.shields.io/badge/language-python-brightgreen.svg)](https://www.python.org/)
[![Documentation Status](https://readthedocs.org/projects/gedmatch-tools/badge/?version=latest)](http://gedmatch-tools.readthedocs.io/en/latest/?badge=latest)


gedmatch-tools
====

**This repository is no longer maintained.  It also has not been tested or used on any recent (2020 or beyond) version of GEDMatch.  Please do not expect support or responses.** 

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

See the [Usage](https://gedmatch-tools.readthedocs.io/en/latest/usage.html) for example tool usage .

See the [API](https://gedmatch-tools.readthedocs.io/en/latest/api.html) for using `gedmatch-tools` programatically.

## Items to be completed prior to an initial release

- [ ] remaining features
  - [ ] add github issues for other applications/routes (user-requests?)
- [ ] packaging and distribution
  - [ ] bioconda
  - [ ] pypi
- [ ] testing
  - [ ] set up travis-ci, including testing email/password for logging into the GEDMatch site
  - [ ] uni testing
    - [ ] parsing credentials (`.gedmatch` file, environment variables)
    - [ ] getting to the main page (`gedmatch_tools.util.main_page()`)
    - [ ] adding a kit or kits (`gedmatch_tools.tools.add.*`)
    - [ ] listing already added/uploaded kits (`gedmatch_tools.tools.ls`)
    - [ ] delete kit or kits ( `gedmatch_tools.tools.rm`)
    - [ ] perform one or more 1:1 autosomal analyses (`gedmatch_tools.tools.one_to_one`)
    - [ ] perform one or more 1:many autosomal analyses (`gedmatch_tools.tools.one_to_many`)
