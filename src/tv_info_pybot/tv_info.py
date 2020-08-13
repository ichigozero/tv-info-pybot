import re


class TvInfoExtractor:
    def _extract_program_title(self, raw_title):
        return re.sub(r'\[.\]', '', raw_title)

    def _extract_channel_name(self, raw_description):
        return re.search(r'\[(.+)\]', raw_description).group(1)
