from datetime import datetime

from bs4 import BeautifulSoup


def test_extract_program_summary(rss_file, tv_info_extractor):
    parsed_rss = BeautifulSoup(rss_file, 'xml')
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
