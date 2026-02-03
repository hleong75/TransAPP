import unittest

from transapp.bootstrap import build_planner
from transapp.config import AppConfig
from transapp.evaluation import Evaluator


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.config = AppConfig(base_dir=self._temp_dir())

    def _temp_dir(self):
        from pathlib import Path
        import tempfile

        return Path(tempfile.mkdtemp())

    def test_planner_selects_fastest_route(self):
        planner = build_planner(self.config)
        route = planner.plan("A", "C")
        self.assertEqual(route.total_duration, 3.0)
        self.assertIn("bike", route.modes)

    def test_evaluator_computes_coverage(self):
        planner = build_planner(self.config)
        evaluator = Evaluator(planner)
        report = evaluator.evaluate([("A", "B"), ("A", "C"), ("X", "Y")])
        self.assertEqual(report.routes_tested, 2)
        self.assertLess(report.coverage_ratio, 1.0)


if __name__ == "__main__":
    unittest.main()
