from plugin import AutograderTestReport, AutograderTestOutcome
from typing import Any


def get_edstem_json(autograder_reports: list[AutograderTestReport]) -> dict[str, Any]:
    output = {"testcases": []}
    for report in autograder_reports:
        testcase = {
            "name": report.name,
            "hidden": False,
            "private": False,
            "score": report.weight,
            "ok": True,
            "passed": report.outcome == AutograderTestOutcome.PASSED,
            "output": report.output,
        }
        output["testcases"].append(testcase)
    return output


def get_gradescope_json(
    autograder_reports: list[AutograderTestReport],
) -> dict[str, Any]:
    output = {}
    return output
