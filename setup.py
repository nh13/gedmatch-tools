from setuptools import setup, find_packages
import sys

if sys.version_info < (3,6):
        sys.exit('Sorry, Python < 3.6 is not supported')

# Get the package version
exec(open('src/python/gedmatch_tools/version.py').read())
setup(
    name = "gedmatch-tools",
    author = "Nils Homer",
    author_email = "nilshomer@gmail.com",
    version = __version__,
    description = "Tools and API for working with GEDMatch (gedmatch.com).",
    url = "https://github.com/nh13/gedmatch-tools",
    license = "MIT",
    #packages = ['gedmatch_tools'],
    #package_dir = {'gedmatch_tools':'src/python/gedmatch_tools'},
	packages = find_packages(where='src/python/'),
	package_dir = {'': 'src/python/'},
    install_requires = ['attrs>=17.4.0', 'selenium>=3.11.0', 'lxml>=4.3.2'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points = {
        'console_scripts': [
            'gedmatch-tools=gedmatch_tools.__main__:main'
        ]
    },
    zip_safe = False,
)
