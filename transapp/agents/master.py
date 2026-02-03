from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from transapp.agents.architect import ArchitectAgent
from transapp.agents.builder import BuilderAgent
from transapp.agents.optimizer import OptimizerAgent
from transapp.agents.reviewer import ReviewerAgent
from transapp.agents.validator import ValidatorAgent
from transapp.agents.base import Proposal
from transapp.evaluation import EvaluationReport


@dataclass(frozen=True)
class MasterReport:
    evaluation: EvaluationReport
    proposals: tuple[Proposal, ...]


class MasterAgent:
    """Coordinate AI agents for self-improvement."""

    def __init__(self) -> None:
        self._agents = (
            ArchitectAgent(),
            BuilderAgent(),
            ReviewerAgent(),
            ValidatorAgent(),
            OptimizerAgent(),
        )

    def run(self, report: EvaluationReport) -> MasterReport:
        proposals = []
        for agent in self._agents:
            proposals.extend(list(agent.propose(report)))
        return MasterReport(evaluation=report, proposals=tuple(proposals))
