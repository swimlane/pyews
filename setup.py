from setuptools import setup, find_packages

setup(
    name='pyews',
    version='0.1.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package to interact with both on-premises and Office 365 Exchange Web Services',
    long_description=open('README.md').read(),
    install_requires=[],
    url='',
    author='Josh Rickard',
    author_email='josh.rickard@swimlane.com'
)