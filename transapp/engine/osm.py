from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class OSMEdge:
    origin: str
    destination: str
    mode: str
    duration_min: float


class OSMNetwork:
    """Minimal offline-ready OSM network representation."""

    def __init__(self, edges: Iterable[OSMEdge]) -> None:
        self._edges = tuple(edges)
        self._adjacency: dict[str, list[OSMEdge]] = {}
        for edge in self._edges:
            self._adjacency.setdefault(edge.origin, []).append(edge)

    @property
    def nodes(self) -> set[str]:
        nodes = {edge.origin for edge in self._edges}
        nodes.update(edge.destination for edge in self._edges)
        return nodes

    @property
    def edges(self) -> tuple[OSMEdge, ...]:
        return self._edges

    def neighbors(self, node: str) -> list[OSMEdge]:
        return list(self._adjacency.get(node, []))

    def to_path(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [edge.__dict__ for edge in self._edges]
        path.write_text(json.dumps(payload, indent=2))

    @classmethod
    def from_path(cls, path: Path) -> "OSMNetwork":
        payload = json.loads(path.read_text())
        return cls(OSMEdge(**edge) for edge in payload)


class OSMDownloader:
    """Offline-friendly downloader stub for vector maps."""

    def __init__(self, url: str, output_path: Path) -> None:
        self.url = url
        self.output_path = output_path

    def download(self) -> OSMNetwork:
        # Placeholder dataset to keep offline deterministic behavior.
        network = OSMNetwork(
            [
                OSMEdge("A", "B", "walk", 7.0),
                OSMEdge("B", "C", "walk", 4.0),
                OSMEdge("A", "C", "bike", 3.0),
            ]
        )
        network.to_path(self.output_path)
        return network
