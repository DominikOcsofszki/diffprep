from collections.abc import Generator

import pytest
from typer.testing import CliRunner

from diffprep.core import (
    JsonSettings,
    NormalizeSettings,
    Settings,
    XmlSettings,
    get_settings,
)


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Generator:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        normalize=NormalizeSettings(trailing_newline=True),
        json_settings=JsonSettings(
            drop_keys=set(),
            indent=None,
            sort_keys=True,
            ensure_ascii=False,
            style="compact",
        ),
        xml_settings=XmlSettings(),
    )
