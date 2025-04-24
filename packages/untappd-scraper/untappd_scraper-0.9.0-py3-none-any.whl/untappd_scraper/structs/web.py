"""Structures from page scraping."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from untappd_scraper.structs.mixins import BeerStrMixin

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Collection
    from datetime import date, datetime

    from untappd_scraper.structs.other import Location


@dataclass(frozen=True)
class WebBeerDetails:
    """A beer web page."""

    beer_id: int
    name: str = field(compare=False)
    description: str = field(compare=False)
    brewery: str = field(compare=False)
    brewery_slug: str = field(compare=False)
    style: str = field(compare=False)
    url: str = field(compare=False)
    num_ratings: int = field(compare=False)
    global_rating: float | None = field(compare=False, default=None)


@dataclass(frozen=True)
class WebBreweryDetails:
    """A brewery web page."""

    brewery_id: int
    name: str = field(compare=False)
    brewery_slug: str = field(compare=False)
    style: str = field(compare=False)
    description: str = field(compare=False)
    num_beers: int = field(compare=False)
    rating: float | None = field(compare=False)
    address: str = field(compare=False)
    url: str = field(compare=False)


@dataclass(frozen=True)
class WebActivityBeer:
    """A checkin from a user or venue activity feed."""

    checkin_id: int
    checkin: datetime = field(compare=False)
    user_name: str = field(compare=False)
    name: str = field(compare=False)
    beer_id: int = field(compare=False)
    beer_label_url: str = field(compare=False)
    brewery_id: int = field(compare=False)
    brewery: str = field(compare=False)
    brewery_slug: str = field(compare=False)
    location: str | None = field(compare=False, default=None)
    location_id: int | None = field(compare=False, default=None)
    purchased_at: str | None = field(compare=False, default=None)
    purchased_id: int | None = field(compare=False, default=None)
    comment: str | None = field(compare=False, default=None)
    serving: str | None = field(compare=False, default=None)
    user_rating: float | None = field(compare=False, default=None)
    friends: list[str] | None = field(compare=False, default=None)

    def __str__(self) -> str:
        """Create a summary description of a beer.

        Returns:
            str: beer description
        """
        summary = (
            f"{self.checkin.astimezone().strftime('%a %H:%M')}: {self.user_name} - "
            f"{self.name} by {self.brewery}"
        )
        if self.location:
            summary += f" at {self.location}"
        if self.serving:
            summary += f" ({self.serving})"
        if self.user_rating:
            summary += f", user rating {self.user_rating}"
        if self.friends:
            friends = ", ".join(self.friends)
            summary += f" with {friends}"
        return summary


@dataclass(frozen=True)
class WebUserDetails:
    """A user's details from the user's web page."""

    user_id: str
    name: str = field(compare=False)
    location: str = field(compare=False)
    url: str = field(compare=False)
    total_beers: int = field(compare=False)
    total_uniques: int = field(compare=False)
    total_badges: int = field(compare=False)
    total_friends: int = field(compare=False)


@dataclass(frozen=True)
class WebUserHistoryBeer(BeerStrMixin):
    """A beer from the user's beer history web page."""

    beer_id: int
    name: str = field(compare=False)
    beer_label_url: str = field(compare=False)
    brewery_id: int = field(compare=False)
    brewery: str = field(compare=False)
    brewery_slug: str = field(compare=False)
    style: str = field(compare=False)
    url: str | None = field(compare=False)
    first_checkin: datetime = field(compare=False)
    first_checkin_id: int = field(compare=False)
    recent_checkin: datetime = field(compare=False)
    recent_checkin_id: int = field(compare=False)
    total_checkins: int = field(compare=False)
    user_rating: float | None = field(compare=False, default=None)
    global_rating: float | None = field(compare=False, default=None)
    abv: float | None = field(compare=False, default=None)
    ibu: int | None = field(compare=False, default=None)


@dataclass(frozen=True)
class WebUserHistoryVenue:
    """User's recent venue."""

    venue_id: int
    name: str = field(compare=False)
    url: str = field(compare=False)
    category: str = field(compare=False)
    address: str = field(compare=False)
    first_visit: date | None = field(compare=False)
    last_visit: date = field(compare=False)
    num_checkins: int = field(compare=False)
    first_checkin_id: int | None = field(compare=False)
    last_checkin_id: int = field(compare=False)


@dataclass(frozen=True)
class WebVenueDetails:
    """A venue web page."""

    venue_id: int
    name: str = field(compare=False)
    verified: bool = field(compare=False)
    venue_slug: str = field(compare=False)
    categories: set[str] = field(compare=False)
    address: str = field(compare=False)
    location: Location | None = field(compare=False)
    url: str = field(compare=False)

    @property
    def activity_url(self) -> str:
        """Return activity page url for this venue.

        For unverified, it's just the main venue page.
        Otherwise there's a 'more activity' link to follow.

        Returns:
            str: venue's activity page url
        """
        return f"{self.url}/activity" if self.verified else self.url


@dataclass(frozen=True)
class WebVenueMenu:
    """Verified venue's menu page(s)."""

    menu_id: int
    selection: str = field(compare=False)
    name: str = field(compare=False)
    description: str = field(compare=False)
    beers: Collection[WebVenueMenuBeer] = field(compare=False, default_factory=set)

    @property
    def full_name(self) -> str:
        """Concatenate menu selector with name to ensure a unique name.

        Returns:
            str: full menu name
        """
        return f"{self.selection} / {self.name}"


@dataclass(frozen=True)
class WebVenueMenuBeer(BeerStrMixin):
    """Beers within a menu."""

    beer_id: int
    name: str = field(compare=False)
    beer_label_url: str = field(compare=False)
    brewery_id: int = field(compare=False)
    brewery: str = field(compare=False)
    style: str = field(compare=False)
    url: str | None = field(compare=False)
    serving: str | None = field(compare=False)
    prices: list[str] = field(compare=False)
    global_rating: float | None = field(compare=False, default=None)
    abv: float | None = field(compare=False, default=None)
    ibu: int | None = field(compare=False, default=None)
