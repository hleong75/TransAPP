from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from transapp.engine.router import RouteOption, RoutePlanner


@dataclass(frozen=True)
class EvaluationReport:
    routes_tested: int
    avg_duration: float
    coverage_ratio: float
    modes_supported: tuple[str, ...]
    storage_estimate_mb: float
    stability_score: float


class Evaluator:
    """Evaluate offline routing performance and coverage."""

    STORAGE_ESTIMATE_MB = 2.5

    def __init__(self, planner: RoutePlanner) -> None:
        self.planner = planner

    def evaluate(self, scenarios: Iterable[tuple[str, str]]) -> EvaluationReport:
        scenarios_list = list(scenarios)
        options: list[RouteOption] = []
        failures = 0
        for origin, destination in scenarios_list:
            try:
                options.append(self.planner.plan(origin, destination))
            except ValueError:
                failures += 1
        avg_duration = (
            sum(option.total_duration for option in options) / len(options)
            if options
            else 0.0
        )
        total = len(scenarios_list)
        coverage_ratio = 0.0 if not total else (len(options) / total)
        modes = tuple(sorted(self.planner.available_modes()))
        storage_estimate_mb = self.STORAGE_ESTIMATE_MB
        stability_score = max(0.0, 1.0 - failures / max(1, len(options) + failures))
        return EvaluationReport(
            routes_tested=len(options),
            avg_duration=avg_duration,
            coverage_ratio=coverage_ratio,
            modes_supported=modes,
            storage_estimate_mb=storage_estimate_mb,
            stability_score=stability_score,
        )
