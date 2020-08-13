import re


class TvInfoExtractor:
    def _extract_program_title(self, raw_title):
        return re.sub(r'\[.\]', '', raw_title)
