import os

import pytest

from tv_info_pybot import TvInfoExtractor


def test_file(filename):
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
    )
    with open(os.path.join(path, filename), 'r') as f:
        return f.read()


@pytest.fixture(scope='module')
def rss_data():
    return test_file('rss.xml').encode('utf-8')


@pytest.fixture
def tv_info_extractor():
    return TvInfoExtractor()
