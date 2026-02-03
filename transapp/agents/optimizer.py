from __future__ import annotations

from transapp.agents.base import Agent, Proposal
from transapp.evaluation import EvaluationReport


class OptimizerAgent(Agent):
    role = "optimizer"

    def propose(self, report: EvaluationReport):
        if report.storage_estimate_mb > 10:
            yield Proposal(
                title="Compression",
                summary="Compresser les assets et purger les anciennes versions.",
                diff="Ajouter un job de compression dans le pipeline.",
            )
