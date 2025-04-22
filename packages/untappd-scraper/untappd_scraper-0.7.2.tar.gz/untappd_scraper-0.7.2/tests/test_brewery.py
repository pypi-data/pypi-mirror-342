"""Test brewery scraping."""

from __future__ import annotations

import pytest

from untappd_scraper.brewery import Brewery
from untappd_scraper.constants import UNTAPPD_BREWERY_HISTORY_SIZE

# ----- Tests -----


@pytest.mark.webtest
def test_brewery_lookup() -> None:
    result = Brewery.from_name("big niles")

    assert result
    assert "Niles" in result.name
    assert "dalmeny" in result.address.casefold()


@pytest.mark.webtest
def test_brewery_buckettys() -> None:
    result = Brewery(484738)  # Bucketty's

    assert result
    assert "bucketty" in result.name.casefold()
    assert "brookvale" in result.address.casefold()
    assert result.style
    assert result.description


@pytest.mark.webtest
def test_brewery_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid brewery ID"):
        Brewery(1234567890)


@pytest.mark.webtest
def test_brewery_invalid_name() -> None:
    result = Brewery.from_name("Koneko and Sylvester")

    assert result is None


@pytest.mark.webtest
def test_brewery_activity() -> None:
    result = Brewery(446724).activity()  # MCBC

    assert result
    assert len(result) == UNTAPPD_BREWERY_HISTORY_SIZE
    assert all("mountain" in r.brewery.casefold() for r in result)
    assert any(r.friends for r in result)
    assert any(r.purchased_at for r in result)
    assert not any("purchased" in r.purchased_at.casefold() for r in result if r.purchased_at)
