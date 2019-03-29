from setuptools import setup, find_packages

setup(
    name='pyews',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package to interact with both on-premises and Office 365 Exchange Web Services',
    long_description=open('README.md').read(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml',
        'pyyaml'
    ],
    keywords='ews exchange office365 email ediscovery+',
    url='',
    author='Josh Rickard',
    author_email='josh.rickard@swimlane.com'
)