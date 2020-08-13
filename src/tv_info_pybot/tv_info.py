import datetime
import re


class TvInfoExtractor:
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
        start_datetime = (
            datetime
            .datetime
            .strptime(raw_date, "%Y-%m-%dT%H:%M%z")
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
