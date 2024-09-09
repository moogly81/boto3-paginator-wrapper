from setuptools import setup, find_packages

setup(
    name='boto3-paginator-wrapper',
    version='0.1',
    packages=find_packages(),
    install_requires=['boto3'],
    description='A simple boto3 wrapper to handle pagination automatically or manually.',
    url='https://github.com/moogly81/boto3-paginator-wrapper',
    author='BURZCE',
    author_email='burzce@gmail.com',
    license='MIT',
)
