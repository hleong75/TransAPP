from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
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
        frontier: list[tuple[float, str, tuple[str, ...]]] = [(0.0, origin, ())]
        best: dict[str, float] = {origin: 0.0}
        while frontier:
            total, node, modes = heappop(frontier)
            if node == destination:
                yield RouteOption(origin, destination, total, tuple(modes), tuple(modes))
                return
            if total > best.get(node, float("inf")):
                continue
            for edge in self.network.neighbors(node):
                new_total = total + edge.duration_min
                if new_total < best.get(edge.destination, float("inf")):
                    best[edge.destination] = new_total
                    heappush(
                        frontier,
                        (new_total, edge.destination, modes + (edge.mode,)),
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
