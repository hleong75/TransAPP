from __future__ import annotations

from transapp.config import AppConfig
from transapp.engine.gtfs import GTFSDownloader, GTFSFeed
from transapp.engine.osm import OSMDownloader, OSMNetwork
from transapp.engine.router import RoutePlanner


def bootstrap_data(config: AppConfig) -> tuple[OSMNetwork, GTFSFeed]:
    """Download or load offline datasets."""
    config.base_dir.mkdir(parents=True, exist_ok=True)
    if config.osm_path.exists():
        network = OSMNetwork.from_path(config.osm_path)
    else:
        network = OSMDownloader(config.osm_url, config.osm_path).download()

    if config.gtfs_path.exists():
        feed = GTFSFeed.from_path(config.gtfs_path)
    else:
        feed = GTFSDownloader(config.gtfs_url, config.gtfs_path).download()

    return network, feed


def build_planner(config: AppConfig) -> RoutePlanner:
    network, feed = bootstrap_data(config)
    return RoutePlanner(network=network, feed=feed)
