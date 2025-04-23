import sys
from pathlib import Path
import shutil
import pyright_to_gitlab_ci.main as dut

TESTS = Path(__file__).resolve().parent
REPORTS = TESTS / "reports"
# pyright is expected to produce abs path, so put it all in /tmp
TMP = Path("/tmp")


def call_pyright_to_gitlab_ci(*argv):
    prev_sys_argv = sys.argv
    try:
        sys.argv = ["pyright-to-gitlab-ci"] + list(argv)
        dut.main()
    finally:
        sys.argv = prev_sys_argv


class TestReportsConversion:
    # automatically populated with the reports
    # in the reports/ directory.
    # each of these being a testcase with an
    # input and an output
    pass


def check_report_produced_correctly(
    f_source, f_input, f_expected_out, f_actual_out, base_path
):
    def _check(self):
        tmp_source = TMP / f_source.name
        shutil.copy(f_source, tmp_source)
        call_pyright_to_gitlab_ci(
            "--src",
            str(f_input),
            "--output",
            str(f_actual_out),
            "--base-path",
            str(base_path),
        )
        with open(f_expected_out) as f:
            expected_out = f.read()
        with open(f_actual_out) as f:
            actual_out = f.read()
        assert expected_out == actual_out

    return _check


for f_source in REPORTS.glob("*.py"):
    f_input = f_source.with_suffix(".pyright.json")
    f_expected_out = f_source.with_suffix(".expected.json")
    f_actual_out = TMP / f_source.with_suffix(".actual.json").name
    base_path = TMP
    if f_source.is_file() and f_expected_out.is_file():
        setattr(
            TestReportsConversion,
            f"test_reports_{f_input.with_suffix('').name}",
            check_report_produced_correctly(
                f_source, f_input, f_expected_out, f_actual_out, base_path
            ),
        )
