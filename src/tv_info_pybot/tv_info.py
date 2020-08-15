import urllib.parse
import datetime
import itertools
import re
from datetime import timedelta

import requests
import tweepy
from bs4 import BeautifulSoup


class TvInfoExtractor:
    def extract_program_summaries_of_multiple_actors(self, actor_names):
        output = []
        for actor_name in actor_names:
            output.append(self.extract_program_summaries(actor_name))

        return list(itertools.chain(*output))

    def extract_program_summaries(self, actor_name):
        rss_data = self._fetch_rss_data(actor_name)
        summaries = []
        try:
            for rss_item in rss_data.find_all('item'):
                summary = self._extract_program_summary(
                    actor_name=actor_name,
                    rss_item=rss_item
                )
                summaries.append(summary)
        except AttributeError:
            pass

        return summaries

    def _fetch_rss_data(self, actor_name):
        try:
            content = requests.get(self._compose_url(actor_name)).content
            return BeautifulSoup(content, 'xml')
        except requests.exceptions.RequestException:
            return None

    def _compose_url(self, actor_name):
        escaped_name = urllib.parse.quote(actor_name)
        return (
            'https://www.tvkingdom.jp/rss/'
            'schedulesBySearch.action?'
            'condition.keyword={}&'
            'stationPlatformId=0'
        ).format(escaped_name)

    def _extract_program_summary(self, actor_name, rss_item):
        return {
            'actor_name': actor_name,
            'title': self._extract_program_title(
                rss_item.title.get_text(strip=True)),
            'channel': self._extract_channel_name(
                rss_item.description.get_text(strip=True)),
            'schedule': self._extract_program_schedule(
                raw_date=rss_item.date.get_text(strip=True),
                raw_description=rss_item.description.get_text(strip=True)
            )
        }

    def _extract_program_title(self, raw_title):
        return re.sub(r'\[.\]', '', raw_title)

    def _extract_channel_name(self, raw_description):
        return re.search(r'\[(.+)\]', raw_description).group(1)

    def _extract_program_schedule(self, raw_date, raw_description):
        end_time = re.search(
            r'[0-9]+\/[0-9]+\s[0-9]+:[0-9]+～([0-9]+):([0-9]+)',
            raw_description
        )
        stripped_date = raw_date.replace(':', '')
        start_datetime = (
            datetime
            .datetime
            .strptime(stripped_date, "%Y-%m-%dT%H%M%z")
            .replace(tzinfo=None)
        )
        end_datetime = datetime.datetime(
            start_datetime.year,
            start_datetime.month,
            start_datetime.day,
            int(end_time.group(1)),
            int(end_time.group(2))
        )

        return {
            'start': start_datetime,
            'end': end_datetime
        }


class TvInfoTweeter:
    def __init__(
            self,
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
    ):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self._tweepy = tweepy.API(auth)

    def tweet_tomorrow_program(self, program_summary):
        tweet_text = self._compose_tomorrow_tweet_text(program_summary)
        if tweet_text:
            try:
                self._tweepy.update_status(tweet_text)
            except tweepy.error.TweepError:
                pass

    def tweet_next_30_minutes_program(self, program_summary):
        tweet_text = self._compose_next_30_minutes_tweet_text(program_summary)
        if tweet_text:
            try:
                self._tweepy.update_status(tweet_text)
            except tweepy.error.TweepError:
                pass

    def _compose_tomorrow_tweet_text(self, program_summary):
        start_datetime = program_summary['schedule']['start']
        now = datetime.datetime.now()
        next_30_minutes = now + timedelta(minutes=30)

        if (now.hour >= 23
                and now.minute >= 30
                and start_datetime > next_30_minutes):
            return self._compose_tweet_text(
                program_summary=program_summary,
                extra_text='明日、よろしくおねがいします。'
            )
        else:
            return ''

    def _compose_next_30_minutes_tweet_text(self, program_summary):
        start_datetime = program_summary['schedule']['start']
        next_30_minutes = datetime.datetime.now() + timedelta(minutes=30)

        if datetime.datetime.now() < start_datetime <= next_30_minutes:
            return self._compose_tweet_text(
                program_summary=program_summary,
                extra_text='まもなく放送開始です！'
            )
        else:
            return ''

    def _compose_tweet_text(self, program_summary, extra_text):
        template = (
            'Botからお知らせ\n'
            '\n'
            '【出演情報】\n'
            '{actor_name}\n'
            '{start_datetime}〜\n'
            '{title}\n'
            '{channel}\n'
            '\n'
            '{extra_text}'
        )
        start_datetime = program_summary['schedule']['start']

        return template.format(
            actor_name=program_summary['actor_name'],
            start_datetime=start_datetime.strftime('%-m/%d %H:%M'),
            title=program_summary['title'],
            channel=program_summary['channel'],
            extra_text=extra_text
        )
