from __future__ import annotations

from transapp.agents.base import Agent, Proposal
from transapp.evaluation import EvaluationReport


class ValidatorAgent(Agent):
    role = "validator"

    def propose(self, report: EvaluationReport):
        if report.stability_score < 0.9:
            yield Proposal(
                title="Renforcer la robustesse",
                summary="Ajouter des règles déterministes de fallback.",
                diff="Exécuter un routage walking-only si GTFS échoue.",
            )
