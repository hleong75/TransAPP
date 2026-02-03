from __future__ import annotations

from transapp.agents.base import Agent, Proposal
from transapp.evaluation import EvaluationReport


class BuilderAgent(Agent):
    role = "builder"

    def propose(self, report: EvaluationReport):
        if report.coverage_ratio < 1.0:
            yield Proposal(
                title="Étendre les scénarios",
                summary="Ajouter des trajets de test pour mieux couvrir le réseau.",
                diff="Étendre la suite de tests d'intégration.",
            )
