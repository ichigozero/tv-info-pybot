# TV Info PyBot
Python port of [tv-info-bot](https://github.com/ikeay/tv-info-bot) originally written in ruby.\
This tool allows you to tweet about Japanese actor/actress appearance
in Japanese television programs.

# Installation
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install .
```

# Usage
1. Add `Twitter API keys` to environment variables.
  ```bash
  export TWITTER_CONSUMER_KEY="your-twitter-consumer-key"
  export TWITTER_CONSUMER_SECRET="your-twitter-consumer-secret"
  export TWITTER_ACCESS_TOKEN="your-twitter-access-token"
  export TWITTER_ACCESS_TOKEN_SECRET="your-twitter-access-token-secret"
  ```

2. Run the following command
  ```bash
  $ tv_info_pybot tweet-batch ACTOR_NAME
  ```

  where,
  * `ACTOR_NAME`: The name of actor/actress you want to tweet about.

  For example,
  ```bash
  $ tv_info_pybot tweet-batch 池澤あやか
  ```
