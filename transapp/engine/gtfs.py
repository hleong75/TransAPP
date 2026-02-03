from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class GTFSTrip:
    trip_id: str
    origin: str
    destination: str
    departure_min: int
    duration_min: int
    mode: str


class GTFSFeed:
    """Minimal offline-ready GTFS feed."""

    def __init__(self, trips: Iterable[GTFSTrip]) -> None:
        self._trips = tuple(trips)
        self._by_origin: dict[str, list[GTFSTrip]] = {}
        for trip in self._trips:
            self._by_origin.setdefault(trip.origin, []).append(trip)

    @property
    def trips(self) -> tuple[GTFSTrip, ...]:
        return self._trips

    def trips_from(self, origin: str) -> list[GTFSTrip]:
        return list(self._by_origin.get(origin, []))

    def to_path(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [trip.__dict__ for trip in self._trips]
        path.write_text(json.dumps(payload, indent=2))

    @classmethod
    def from_path(cls, path: Path) -> "GTFSFeed":
        payload = json.loads(path.read_text())
        return cls(GTFSTrip(**trip) for trip in payload)


class GTFSDownloader:
    """Offline-friendly downloader stub for GTFS archives."""

    def __init__(self, url: str, output_path: Path) -> None:
        self.url = url
        self.output_path = output_path

    def download(self) -> GTFSFeed:
        feed = GTFSFeed(
            [
                GTFSTrip("T1", "A", "B", 0, 5, "metro"),
                GTFSTrip("T2", "B", "C", 6, 6, "tram"),
                GTFSTrip("T3", "A", "C", 3, 9, "bus"),
            ]
        )
        feed.to_path(self.output_path)
        return feed
