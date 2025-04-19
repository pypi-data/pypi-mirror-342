import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from netorca_sdk.junit_reporter import JUnitReporter


@pytest.fixture
def reporter(tmp_path: Path) -> JUnitReporter:
    return JUnitReporter(output_path=f"{tmp_path}/junit.xml")


def test_format_reason_simple(reporter: JUnitReporter) -> None:
    reason = {"billing_code": "'billing_code' is a required property"}
    output = reporter._format_reason(reason, "metadata")
    assert "billing_code" in output
    assert "required property" in output


def test_format_reason_nested(reporter: JUnitReporter) -> None:
    reason = {"state": "invalid", "extra": {"foo": "must be int"}}
    output = reporter._format_reason(reason, "simple_rule")
    assert "state" in output
    assert "extra.foo" in output


def test_format_table_empty() -> None:
    output = JUnitReporter._format_table(("Field", "Reason"), [])
    assert output == ""


def test_write_creates_file(tmp_path: Path) -> None:
    output_file = tmp_path / "junit.xml"
    reporter = JUnitReporter(output_path=str(output_file))
    errors = {
        "repo": {
            "alpha": {
                "metadata": {"billing_code": "'billing_code' is a required property"},
                "core": {"simple_rule": {"state": "invalid"}},
            }
        }
    }
    reporter.write(errors)
    assert output_file.exists()
    tree = ET.parse(output_file)
    root = tree.getroot()
    assert root.tag == "testsuite"
    testcases = list(root.findall("testcase"))
    assert len(testcases) == 2
    names = [tc.attrib["name"] for tc in testcases]
    assert "alpha - metadata" in names
    assert "alpha - core" in names
