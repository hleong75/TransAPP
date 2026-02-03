from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

from transapp.engine.gtfs import GTFSFeed, GTFSTrip
from transapp.engine.osm import OSMNetwork, OSMEdge


@dataclass(frozen=True)
class RouteOption:
    origin: str
    destination: str
    total_duration: float
    modes: tuple[str, ...]
    steps: tuple[str, ...]


class RoutePlanner:
    """Multimodal route planner using preloaded offline data."""

    def __init__(self, network: OSMNetwork, feed: GTFSFeed) -> None:
        self.network = network
        self.feed = feed

    def _walk_routes(self, origin: str, destination: str) -> Iterable[RouteOption]:
        frontier = deque([(origin, 0.0, ())])
        visited = set()
        while frontier:
            node, total, modes = frontier.popleft()
            if node == destination:
                yield RouteOption(origin, destination, total, tuple(modes), tuple(modes))
                continue
            if node in visited:
                continue
            visited.add(node)
            for edge in self.network.neighbors(node):
                frontier.append(
                    (edge.destination, total + edge.duration_min, modes + (edge.mode,))
                )

    def _gtfs_routes(self, origin: str, destination: str) -> Iterable[RouteOption]:
        for trip in self.feed.trips_from(origin):
            if trip.destination == destination:
                yield RouteOption(
                    origin,
                    destination,
                    trip.duration_min,
                    (trip.mode,),
                    (trip.trip_id,),
                )

    def plan(self, origin: str, destination: str) -> RouteOption:
        """Return the fastest available route option."""
        options: list[RouteOption] = []
        options.extend(self._walk_routes(origin, destination))
        options.extend(self._gtfs_routes(origin, destination))
        if not options:
            raise ValueError(f"No route between {origin} and {destination}")
        return min(options, key=lambda option: option.total_duration)

    def available_modes(self) -> set[str]:
        modes = {edge.mode for edge in self.network.edges}
        modes.update(trip.mode for trip in self.feed.trips)
        return modes
