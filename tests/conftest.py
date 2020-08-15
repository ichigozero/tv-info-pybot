import os
import datetime

import pytest

from tv_info_pybot import TvInfoExtractor
from tv_info_pybot import TvInfoTweeter


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


@pytest.fixture(scope='module')
def fake_datetime_now():
    return datetime.datetime(2020, 7, 28, 23, 30)


@pytest.fixture
def tv_info_extractor():
    return TvInfoExtractor()


@pytest.fixture
def tv_info_tweeter():
    twitter_api_keys = {
        'consumer_key': 'CONSUMER_KEY',
        'consumer_secret': 'CONSUMER_SECRET',
        'access_token': 'ACCESS_TOKEN',
        'access_token_secret': 'ACCESS_TOKEN_SECRET'
    }
    return TvInfoTweeter(twitter_api_keys)
