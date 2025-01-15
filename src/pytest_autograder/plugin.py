import pytest
from pytest_autograder.backends import format_for_edstem
from pathlib import Path


weight = pytest.mark.weight


@pytest.fixture
def submission_path(request):
    return request.config.option.submission_path


_reports = []


def pytest_addoption(parser):
    group = parser.getgroup("autograder")
    group.addoption(
        "--submission-path",
        action="store",
        default=".",
        type=Path,
        help="Autograder submission path.",
        dest="submission_path",
    )
    group.addoption(
        "--output-path",
        action="store",
        default="output.json",
        type=Path,
        help="Autograder output path.",
        dest="output_path",
    )
    group.addoption(
        "--output-format",
        action="store",
        default="edstem",
        type=str,
        choices=["edstem"],
        help="Autograder output format.",
        dest="output_format",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "weight(value): mark test with `value` weight"
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    weight_mark = item.get_closest_marker("weight", weight(0))
    report.weight = weight_mark.args[0]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_logreport(report):
    yield
    if report.when == "call":
        _reports.append(report)


def pytest_unconfigure(config):
    output_path = config.option.output_path
    output_format = config.option.output_format
    if output_format == "edstem":
        output = format_for_edstem(_reports)
        output_path.write_text(output)
