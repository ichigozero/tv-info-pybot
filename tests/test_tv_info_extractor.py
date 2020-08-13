from datetime import datetime

import requests
from bs4 import BeautifulSoup

DUMMY_URL = 'http://localhost'


def test_fetch_rss_data(requests_mock, mocker, rss_data, tv_info_extractor):
    requests_mock.get(DUMMY_URL, content=rss_data)
    mocker.patch(
        target='tv_info_pybot.TvInfoExtractor._compose_url',
        return_value=DUMMY_URL
    )
    expected = BeautifulSoup(rss_data, 'xml')
    output = tv_info_extractor._fetch_rss_data('増田貴久')

    assert output == expected


def test_failing_to_fetch_rss_data(
        requests_mock,
        mocker,
        rss_data,
        tv_info_extractor
):
    requests_mock.get(DUMMY_URL, exc=requests.exceptions.HTTPError)
    mocker.patch(
        target='tv_info_pybot.TvInfoExtractor._compose_url',
        return_value=DUMMY_URL
    )
    output = tv_info_extractor._fetch_rss_data('増田貴久')

    assert output is None


def test_compose_url(tv_info_extractor):
    expected = (
        'https://www.tvkingdom.jp/rss/schedulesBySearch.action?'
        'condition.keyword=%E5%A2%97%E7%94%B0%E8%B2%B4%E4%B9%85&'
        'stationPlatformId=0'
    )
    output = tv_info_extractor._compose_url('増田貴久')

    assert output == expected


def test_extract_program_summary(rss_data, tv_info_extractor):
    parsed_rss = BeautifulSoup(rss_data, 'xml')
    rss_item = parsed_rss.item
    expected = {
        'actor_name': '増田貴久',
        'title': (
            'ネタパレ【爆笑新作!ミキ・四千頭身・'
            'ラランド・蛙亭・トット・サンシャイン他】'
        ),
        'channel': 'フジテレビ(Ch.8)',
        'schedule': {
            'start': datetime(2020, 8, 14, 23, 40),
            'end': datetime(2020, 8, 14, 0, 10)
        }
    }
    output = tv_info_extractor._extract_program_summary(
        actor_name='増田貴久',
        rss_item=rss_item
    )

    assert output == expected


def test_extract_program_title(tv_info_extractor):
    raw_title = (
        'ネタパレ【爆笑新作!ミキ・四千頭身・'
        'ラランド・蛙亭・トット・サンシャイン他】[字]'
    )
    expected = (
        'ネタパレ【爆笑新作!ミキ・四千頭身・'
        'ラランド・蛙亭・トット・サンシャイン他】'
    )
    output = tv_info_extractor._extract_program_title(raw_title)

    assert output == expected


def test_extract_channel_name(tv_info_extractor):
    raw_description = '8/14 23:40～0:10 [フジテレビ(Ch.8)]'
    expected = 'フジテレビ(Ch.8)'
    output = tv_info_extractor._extract_channel_name(raw_description)

    assert output == expected


def test_extract_program_schedule(tv_info_extractor):
    raw_description = '8/14 23:40～0:10 [フジテレビ(Ch.8)]'
    raw_date = '2020-08-14T23:40+09:00'
    expected = {
        'start': datetime(2020, 8, 14, 23, 40),
        'end': datetime(2020, 8, 14, 0, 10)
    }
    output = tv_info_extractor._extract_program_schedule(
        raw_date,
        raw_description,
    )

    assert output == expected
