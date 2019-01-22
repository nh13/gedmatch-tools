==============
gedmatch-tools
==============

:Author: Nils Homer
:Date: |today|
:Version: |version|

Tools and Python API for `GEDMatch Genesis <https://genesis.gedmatch.com>`_.

Documentation Contents
======================

.. toctree::
   :maxdepth: 1

   api.rst
   usage.rst
   installation.rst
   release.rst

Installation
============

To install the latest release, type::

    git clone https://github.com/nh13/gedmatch-tools.git
    python setup.py install

See the :ref:`Installation notes <installation>` for details.

GEDMatch.com Credentials
========================

GEDMatch.com credentials can retrieved in two ways:

1. Create a CSV file in `~/.gedmatch` with the following contents::

    email,<your-email>
    password,<your-password>

2. Copy your email and password into the environment variables `GEDMATCH_EMAIL` and `GEDMATCH_PASSWORD` respectively.

Indices and tables
------------------

Contents:

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

References
----------

.. seealso::

   GEDMatch genesis
      http://genesis.gedmatch.com

   The python language
      http://www.python.org
