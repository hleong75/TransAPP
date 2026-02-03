from __future__ import annotations

from transapp.agents.base import Agent, Proposal
from transapp.evaluation import EvaluationReport


class ArchitectAgent(Agent):
    role = "architect"

    def propose(self, report: EvaluationReport):
        summary = (
            "Revoir la granularité des modules et séparer les pipelines de données "
            "pour limiter la mémoire."
        )
        yield Proposal(
            title="Découpage des pipelines",
            summary=summary,
            diff="Créer des workers dédiés pour OSM et GTFS.",
        )
