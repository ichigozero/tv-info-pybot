from datetime import datetime


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
