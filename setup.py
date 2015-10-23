import os
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession

install_reqs = parse_requirements("requirements.txt", session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name = "python_analysis_toolkit",
    version = "0.11.0",
    packages=find_packages(),
    author = "Tommy Carpenter",
    author_email = "tommyjcarpenter@gmail.com",
    description = ("A collection of data-analysis based functions for Python."),
    url = "https://github.com/tommyjcarpenter/python-analysis-toolkit",
    install_requires=reqs
)
