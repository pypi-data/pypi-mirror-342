"""Test user venue history scraping."""

from __future__ import annotations

import pytest

from untappd_scraper.constants import UNTAPPD_VENUE_HISTORY_SIZE
from untappd_scraper.user_venue_history import load_user_venue_history

# ----- Tests -----


@pytest.mark.usefixtures("_mock_user_venue_history_get")
def test_load_user_venue_history() -> None:
    venues = load_user_venue_history("test")
    assert len(venues) == UNTAPPD_VENUE_HISTORY_SIZE

    result = venues[0]

    assert result.name
    assert result.url
