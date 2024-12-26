from setuptools import setup, find_packages

setup(
    name='Project Structure 101',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],  # List your dependencies here
)