from __future__ import annotations

from transapp.agents.master import MasterAgent
from transapp.bootstrap import build_planner
from transapp.config import AppConfig
from transapp.evaluation import Evaluator


def main() -> int:
    config = AppConfig()
    planner = build_planner(config)
    evaluator = Evaluator(planner)
    report = evaluator.evaluate([("A", "B"), ("A", "C"), ("B", "C")])
    master = MasterAgent()
    master_report = master.run(report)

    print("Evaluation:", report)
    print("Proposals:", master_report.proposals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
