"""Setup Digging Into Data.

Although the Digging Into Data package is not a pure Python package,
needing to be unpacked and used in situ, the convention of using setup.py
as the installation method is followed.
"""

import inspect
import os

# Import Distribute / Setuptools
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

from diggingintodata.setup.commands import (develop,
                                            install,
                                            uninstall,
                                            unavailable_command)

_name = 'digging-into-data'
_version = '1.0'

# Inspect to find current path
setuppath = inspect.getfile(inspect.currentframe())
setupdir = os.path.dirname(setuppath)

setup(
    name = _name,
    version = _version,
    description = ('Integrating Data Mining and Data Management Technologies '
                   'for Scholarly Inquiry'),
    packages = ['diggingintodata'],
    requires=['cheshire3'],
    author = 'John Harrison, et al.',
    author_email = u'john.harrison@liv.ac.uk',
    maintainer = 'John Harrison',
    maintainer_email = u'john.harrison@liv.ac.uk',
    license = "BSD",
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Internet :: Z39.50",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: Markup"
    ],
    cmdclass = {
                'bdist_egg': unavailable_command,
                'bdist_rpm': unavailable_command,
                'bdist_wininst': unavailable_command,
                'develop': develop,
                'install': install,
                'uninstall': uninstall,
                },
)
