#!/bin/python3

import warnings
import os
from setuptools import setup, find_packages

__version__ = None
exec(open('conservation/version.py').read())

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(
  name='conservation',
  packages=find_packages(),
  version=__version__,
  license='MIT',
  description='Evolutionary Conservation of Amino Acids and Codons',
  long_description=read_file('README.md'),
  long_description_content_type='text/markdown',
  author='Hanjun Lee',
  author_email='hanjun_lee@hms.harvard.edu',
  url='https://github.com/hanjunlee21/conservation',
  download_url='https://github.com/hanjunlee21/conservation/archive/refs/tags/v.' + __version__ + '.tar.gz',
  keywords=['bioinformatics'],
  install_requires=[
      'numpy', 'pandas', 'biopython', 'scipy', 'matplotlib', 'tqdm', 'importlib-resources'
  ],
  python_requires='>=3.6',
  scripts=['bin/conservation'],
  include_package_data=True,
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
