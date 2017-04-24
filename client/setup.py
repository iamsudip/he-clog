from setuptools import setup, find_packages

setup(
    name='clog-client',
    version='0.1',
    packages=find_packages(),
    install_requires = ['thrift==0.9.3'],
    author='Sudip Maji',
    author_email='iamsudip@programmer.net',
)

