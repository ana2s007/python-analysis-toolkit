import os
from setuptools import setup
from pip.req import parse_requirements

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

reqs = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]

setup(
    name = "python_analysis_toolkit",
    version = "0.5.0",
    author = "Tommy Carpenter",
    author_email = "tommyjcarpenter@gmail.com",
    description = ("A collection of data-analysis based functions for Python."),
    license = "TBD",
    keywords = "python",
    url = "https://github.com/tommyjcarpenter/python-analysis-toolkit",
    packages=[],
    long_description=read('README.md'),
    classifiers=[],
    install_requires=reqs
)
