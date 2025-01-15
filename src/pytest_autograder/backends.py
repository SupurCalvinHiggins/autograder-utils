import json
from pytest import TestReport


def format_for_edstem(reports: list[TestReport]) -> dict:
    output = {"testcases": []}
    for report in reports:
        testcase = {
            "name": report.nodeid,
            "hidden": False,
            "private": False,
            "score": report.weight,
            "ok": True,
            "passed": report.outcome == "passed",
            "output": report.longreprtext,
        }
        output["testcases"].append(testcase)
    return json.dumps(output)
