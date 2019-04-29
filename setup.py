from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()

setup(
    name='pyews',
    version='1.0.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package to interact with both on-premises and Office 365 Exchange Web Services',
    long_description=open('README.md').read(),
    install_requires=parse_requirements('./requirements.txt'),
    keywords='ews exchange office365 email ediscovery swimlane',
    url='https://github.com/swimlane/pyews',
    author='Swimlane',
    author_email='info@swimlane.com'
)