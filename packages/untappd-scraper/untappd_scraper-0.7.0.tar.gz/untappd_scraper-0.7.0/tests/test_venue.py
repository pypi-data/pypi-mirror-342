"""Test venue scraping."""

from __future__ import annotations

import pytest

from untappd_scraper.venue import Venue


@pytest.fixture
def venue_unv(_mock_venue_unv_get: None) -> Venue:
    return Venue(14705)


@pytest.fixture
def venue_ver(_mock_venue_ver_get: None) -> Venue:
    return Venue(107565)


@pytest.fixture
def venue_nest(_mock_venue_ver_nest_get: None) -> Venue:
    """Eg, Dad & Daves have a menu pulldown."""
    return Venue(5840988)


# ----- Tests -----


def test_venue(venue_unv: Venue) -> None:
    result = venue_unv

    assert result
    assert result.name
    assert result.venue_id
    assert result.categories


@pytest.mark.usefixtures("_mock_venue_404")
def test_user_invalid() -> None:
    with pytest.raises(ValueError, match="Invalid"):
        Venue(123)  # ignored


def test_menus_unverified(venue_unv: Venue) -> None:
    result = venue_unv.menus()

    assert not result


def test_menus_verified(venue_ver: Venue) -> None:
    menus = venue_ver.menus()
    assert len(menus) == 4

    result = next(iter(menus))

    assert result.beers
    assert result.full_name


def test_menus_nest(venue_nest: Venue) -> None:
    menus = venue_nest.menus()
    # TODO should be more but i think it's caching all the different menus
    assert len(menus) == 4

    result = next(iter(menus))

    assert result.beers
    assert result.full_name


def test_menus_named_verified(venue_ver: Venue) -> None:
    menus = venue_ver.menus("rooftop")
    assert len(menus) == 1

    result = next(iter(menus))

    assert result.name.casefold() == "rooftop"
    assert result.menu_id


def test_activity_unverified(venue_unv: Venue) -> None:
    history = venue_unv.activity()
    assert history
    assert len(history) == 20

    result = next(iter(history))

    assert result.beer_id
    assert result.location
