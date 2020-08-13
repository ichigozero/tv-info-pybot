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
