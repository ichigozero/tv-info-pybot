import datetime

import tweepy


def test_tweet_tomorrow_program(mocker, tv_info_tweeter):
    mocked_composer = mocker.patch.object(
        target=tv_info_tweeter,
        attribute='_compose_tomorrow_tweet_text',
        return_value='bar'
    )
    mocked_tweepy = mocker.patch.object(
        target=tweepy.API,
        attribute='update_status'
    )
    program_summary = {}

    tv_info_tweeter.tweet_tomorrow_program(program_summary)

    mocked_composer.assert_called_once_with(program_summary)
    mocked_tweepy.assert_called_once_with('bar')


def test_tweet_next_30_minutes_program(mocker, tv_info_tweeter):
    mocked_composer = mocker.patch.object(
        target=tv_info_tweeter,
        attribute='_compose_next_30_minutes_tweet_text',
        return_value='bar'
    )
    mocked_tweepy = mocker.patch.object(
        target=tweepy.API,
        attribute='update_status'
    )
    program_summary = {}

    tv_info_tweeter.tweet_next_30_minutes_program(program_summary)

    mocked_composer.assert_called_once_with(program_summary)
    mocked_tweepy.assert_called_once_with('bar')


def test_compose_tomorrow_tweet_text(
        monkeypatch,
        mocker,
        fake_datetime_now,
        tv_info_tweeter
):
    class MockDateTime:
        def now(*args, **kwargs):
            return fake_datetime_now

    program_summary = {
        'schedule': {
            'start': datetime.datetime(2020, 7, 29, 0, 1)
        }
    }

    monkeypatch.setattr(datetime, 'datetime', MockDateTime)
    mocked_composer = mocker.patch.object(
        target=tv_info_tweeter,
        attribute='_compose_tweet_text',
        return_value='bar'
    )

    output = tv_info_tweeter._compose_tomorrow_tweet_text(program_summary)

    mocked_composer.assert_called_once_with(
        program_summary=program_summary,
        extra_text='明日、よろしくおねがいします。'
    )
    assert output == 'bar'


def test_compose_today_tweet_text(
        monkeypatch,
        mocker,
        fake_datetime_now,
        tv_info_tweeter
):
    class MockDateTime:
        def now(*args, **kwargs):
            return fake_datetime_now

    program_summary = {
        'schedule': {
            'start': datetime.datetime(2020, 7, 29, 0, 0)
        }
    }

    monkeypatch.setattr(datetime, 'datetime', MockDateTime)
    spy = mocker.spy(tv_info_tweeter, '_compose_tweet_text')

    output = (
        tv_info_tweeter._compose_tomorrow_tweet_text(program_summary)
    )

    spy.call_count == 0
    assert output == ''


def test_compose_next_30_minutes_tweet_text(
        monkeypatch,
        mocker,
        fake_datetime_now,
        tv_info_tweeter
):
    class MockDateTime:
        def now(*args, **kwargs):
            return fake_datetime_now

    program_summary = {
        'schedule': {
            'start': datetime.datetime(2020, 7, 29, 0, 0)
        }
    }

    monkeypatch.setattr(datetime, 'datetime', MockDateTime)
    mocked_composer = mocker.patch.object(
        target=tv_info_tweeter,
        attribute='_compose_tweet_text',
        return_value='bar'
    )

    output = (
        tv_info_tweeter._compose_next_30_minutes_tweet_text(program_summary)
    )

    mocked_composer.assert_called_once_with(
        program_summary=program_summary,
        extra_text='まもなく放送開始です！'
    )
    assert output == 'bar'


def test_compose_next_31_minutes_tweet_text(
        monkeypatch,
        mocker,
        fake_datetime_now,
        tv_info_tweeter
):
    class MockDateTime:
        def now(*args, **kwargs):
            return fake_datetime_now

    program_summary = {
        'schedule': {
            'start': datetime.datetime(2020, 7, 29, 0, 1)
        }
    }

    monkeypatch.setattr(datetime, 'datetime', MockDateTime)
    spy = mocker.spy(tv_info_tweeter, '_compose_tweet_text')

    output = (
        tv_info_tweeter._compose_next_30_minutes_tweet_text(program_summary)
    )

    spy.call_count == 0
    assert output == ''


def test_compose_tweet_text(tv_info_tweeter):
    program_summary = {
        'actor_name': '池澤あやか',
        'title': '高専ロボコン2019「関東甲信越地区大会」',
        'channel': 'ＮＨＫ総合１・東京(Ch.1)',
        'schedule': {
            'start': datetime.datetime(2019, 11, 17, 13, 5),
            'end': None
        }
    }
    extra_text = '明日、よろしくおねがいします。'
    expected = {
        'Botからお知らせ\n'
        '\n'
        '【出演情報】\n'
        '池澤あやか\n'
        '11/17 13:05〜\n'
        '高専ロボコン2019「関東甲信越地区大会」\n'
        'ＮＨＫ総合１・東京(Ch.1)\n'
        '\n'
        '明日、よろしくおねがいします。'
    }
    output = tv_info_tweeter._compose_tweet_text(
        program_summary=program_summary,
        extra_text=extra_text
    )

    return output == expected
