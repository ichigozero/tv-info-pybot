from setuptools import setup, find_packages

setup(
    name='tv-info-pybot',
    description='Python port of tv-info-bot originally written in ruby',
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'beautifulsoup4',
        'click',
        'lxml',
        'requests',
        'schedule',
        'tweepy'
    ],
    entry_points='''
        [console_scripts]
        tv_info_pybot=tv_info_pybot.__main__:main
    ''',
)
