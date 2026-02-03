from __future__ import annotations

from transapp.agents.base import Agent, Proposal
from transapp.evaluation import EvaluationReport


class ReviewerAgent(Agent):
    role = "reviewer"

    def propose(self, report: EvaluationReport):
        if report.avg_duration > 10:
            yield Proposal(
                title="Optimiser le routage",
                summary="Réduire la latence en mettant en cache les itinéraires.",
                diff="Ajouter un cache LRU dans le planner.",
            )
