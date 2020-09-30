"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup, find_packages
from glob import glob
import os
APP = ['klambda/__main__.py']
DATA_FILES = [('logs',glob("logs/*.log"))]

setup(
    name='klambda',
    version="1.0",
    description="A Klambda program",
    author="falvarado",
    author_email="falvarado@akurey.com",
    packages=find_packages(),
    data_files=DATA_FILES,
    setup_requires=['py2app'],
    include_package_data=True,
    install_requires=['svn', 'boto3', 'pyyaml'],
    python_requires='>=3',
    entry_points = {
        'console_scripts': ['klambda=klambda.__main__:main'],
    }
)
