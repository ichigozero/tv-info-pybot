from setuptools import setup, find_packages

setup(
    name='tv-info-pybot',
    description='Python port of tv-info-bot originally written in ruby',
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
