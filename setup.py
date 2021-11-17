import os
import re

from setuptools import find_packages
from setuptools import setup


def path_in_project(*path):
    return os.path.join(os.path.dirname(__file__), *path)


def read_file(filename):
    with open(path_in_project(filename)) as f:
        return f.read()


def read_requirements(filename):
    contents = read_file(filename).strip('\n')
    return contents.split('\n') if contents else []


def get_version():
    init_path = os.path.join('robozhab', '__init__.py')
    content = read_file(init_path)
    match = re.search(r"__version__ = '([^']+)'", content, re.M)
    version = match.group(1)
    return version


setup(
    name='robozhab',
    version=get_version(),
    packages=find_packages(include=path_in_project('robozhab*'), exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],
    scripts=[
        'robozhab/main.py',
    ],
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('requirements.txt'),
    zip_safe=False,
)
