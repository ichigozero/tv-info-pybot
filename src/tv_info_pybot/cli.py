import os
import time

import click
import schedule

from .tv_info import TvInfoExtractor
from .tv_info import TvInfoTweeter


@click.group()
def cmd():
    pass


@cmd.command()
@click.argument('actor_name')
def tweet_batch(actor_name):
    def _tweet_program_summary(actor_name, twitter_api_keys):
        extractor = TvInfoExtractor()
        tweeter = TvInfoTweeter(twitter_api_keys)

        summaries = extractor.extract_program_summaries(actor_name)
        for summary in summaries:
            tweeter.tweet_next_30_minutes_program(summary)
            tweeter.tweet_tomorrow_program(summary)

    try:
        twitter_api_keys = {
            'consumer_key': os.environ['TWITTER_CONSUMER_KEY'],
            'consumer_secret': os.environ['TWITTER_CONSUMER_SECRET'],
            'access_token': os.environ['TWITTER_ACCESS_TOKEN'],
            'access_token_secret': os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        }

        schedule.every(30).minutes.do(
            _tweet_program_summary,
            actor_name,
            twitter_api_keys
        )
        schedule.run_all()

        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyError:
        click.echo('Some input variables are missing.')
        click.echo('Terminating...')
