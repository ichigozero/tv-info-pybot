import time
import datetime

import schedule
from click.testing import CliRunner

from tv_info_pybot import tweet_batch
from tv_info_pybot import TvInfoExtractor
from tv_info_pybot import TvInfoTweeter


def test_tweet_batch_command_execution(
        monkeypatch,
        mocker,
        fake_datetime_now
):
    class MockDateTime:
        def now(*args, **kwargs):
            return fake_datetime_now

    def _mock_time_sleep():
        exit()

    expected_next_run_datetime = datetime.datetime(2020, 7, 29, 0, 0)

    monkeypatch.setattr(datetime, 'datetime', MockDateTime)
    monkeypatch.setattr(
        target=time,
        name='sleep',
        value=_mock_time_sleep
    )

    twitter_api_keys = {
        'TWITTER_CONSUMER_KEY': 'CONSUMER_KEY',
        'TWITTER_CONSUMER_SECRET': 'CONSUMER_SECRET',
        'TWITTER_ACCESS_TOKEN': 'ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET': 'ACCESS_TOKEN_SECRET'
    }
    for key, value in twitter_api_keys.items():
        monkeypatch.setenv(name=key, value=value)

    summary_extractor_mock = mocker.patch.object(
        target=TvInfoExtractor,
        attribute='extract_program_summaries',
        return_value=['Summary A', 'Summary B']
    )
    half_hour_tweet_mock = mocker.patch.object(
        target=TvInfoTweeter,
        attribute='tweet_next_30_minutes_program'
    )
    tomorrow_tweet_mock = mocker.patch.object(
        target=TvInfoTweeter,
        attribute='tweet_tomorrow_program'
    )

    runner = CliRunner()
    runner.invoke(tweet_batch, ['池澤あやか'])

    summary_extractor_mock.assert_called_once_with('池澤あやか')
    assert half_hour_tweet_mock.call_count == 2
    assert tomorrow_tweet_mock.call_count == 2
    assert schedule.next_run() == expected_next_run_datetime


def test_error_output_returned_by_tweet_batch_command():
    runner = CliRunner()
    result = runner.invoke(tweet_batch, ['池澤あやか'])
    expected_output = (
        'Some input variables are missing.\n'
        'Terminating...\n'
    )

    assert result.output == expected_output
