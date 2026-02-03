from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from transapp.evaluation import EvaluationReport


@dataclass(frozen=True)
class Proposal:
    title: str
    summary: str
    diff: str


class Agent:
    """Base class for orchestration agents."""

    role: str = "agent"

    def propose(self, report: EvaluationReport) -> Iterable[Proposal]:
        """Return improvement proposals based on the evaluation report."""
        raise NotImplementedError
