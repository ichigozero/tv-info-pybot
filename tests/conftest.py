import pytest

from tv_info_pybot import TvInfoExtractor


@pytest.fixture
def tv_info_extractor():
    return TvInfoExtractor()
