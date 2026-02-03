from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Configuration for offline multimodal routing."""

    base_dir: Path = Path("/tmp/transapp")
    osm_url: str = (
        "https://download.geofabrik.de/europe/france/ile-de-france-latest.osm.pbf"
    )
    gtfs_url: str = "https://transport.data.gouv.fr/gtfs.zip"

    @property
    def osm_path(self) -> Path:
        return self.base_dir / "osm" / "network.json"

    @property
    def gtfs_path(self) -> Path:
        return self.base_dir / "gtfs" / "gtfs.json"

    @property
    def state_path(self) -> Path:
        return self.base_dir / "state.json"
