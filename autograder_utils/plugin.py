from __future__ import annotations

import pytest
from dataclasses import dataclass
from enum import Enum, auto


class AutograderTestOutcome(Enum):
    PASSED = auto()
    FAILED = auto()
    SKIPPED = auto()

    @staticmethod
    def from_literal(literal: str) -> AutograderTestOutcome:
        return {
            "passed": AutograderTestOutcome.PASSED,
            "failed": AutograderTestOutcome.FAILED,
            "skipped": AutograderTestOutcome.SKIPPED,
        }[literal]


@dataclass
class AutograderTestReport:
    name: str
    weight: int
    duration: float
    outcome: AutograderTestOutcome
    output: str

    @staticmethod
    def from_report(report: pytest.TestReport) -> AutograderTestReport:
        return AutograderTestReport(
            name=report.nodeid,
            weight=report.weight if report.weight is not None else 0,
            duration=report.duration,
            outcome=AutograderTestOutcome.from_literal(report.outcome),
            output=report.longreprtext,
        )


weight = pytest.mark.weight


class AutograderPlugin:
    def __init__(self):
        self.autograder_reports: list[AutograderTestReport] = []

    def pytest_addoption(self, parser):
        parser.addoption(
            "--autograder-submission-dir",
            action="store",
            default=".",
            help="Submission directory.",
        )

    def pytest_configure(self, config):
        config.addinivalue_line(
            "markers", "weight(value): mark test with `value` weight"
        )

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item):
        outcome = yield
        report = outcome.get_result()
        weight_mark = item.get_closest_marker("weight")
        report.weight = weight_mark.args[0] if weight_mark is not None else None

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_logreport(self, report: pytest.TestReport):
        yield
        if report.when == "call":
            autograder_report = AutograderTestReport.from_report(report)
            self.autograder_reports.append(autograder_report)
