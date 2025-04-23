import os
import sys
from pathlib import Path
from argparse import ArgumentParser
import json
from hashlib import md5
import typing
from typing import Any
from dataclasses import dataclass, asdict
from enum import Enum
import functools
import warnings


@dataclass(eq=True, frozen=True)
class CodeClimatePosition:
    line: int
    column: int


@dataclass(eq=True, frozen=True)
class CodeClimateRange:
    begin: CodeClimatePosition
    end: CodeClimatePosition


@dataclass
class PyrightPosition:
    line: int
    character: int


@dataclass
class PyrightRange:
    start: PyrightPosition
    end: PyrightPosition

    def __init__(self, start: dict[str, int], end: dict[str, int]):
        self.start = PyrightPosition(**start)
        self.end = PyrightPosition(**end)

    def to_positions(self) -> CodeClimateRange:
        return CodeClimateRange(
            begin=CodeClimatePosition(
                line=self.start.line, column=self.start.character
            ),
            end=CodeClimatePosition(line=self.end.line, column=self.end.character),
        )


@dataclass
class PyrightUri:
    _key: str
    _filePath: str


class PyrightSeverityLevel(str, Enum):
    error = "error"
    warning = "warning"
    information = "information"
    unusedcode = "unusedcode"
    unreachablecode = "unreachablecode"
    deprecated = "deprecated"


class GitlabSeverityLevel(str, Enum):
    blocker = "blocker"
    major = "major"
    minor = "minor"
    info = "info"


@dataclass(eq=True, frozen=True)
class GitlabReportLocation:
    path: str
    positions: CodeClimateRange

    @functools.cache
    def get_lines(self, base_path) -> str:
        with open(base_path / self.path, "rt") as f:
            ls = f.readlines()
        return "".join(ls[self.positions.begin.line : self.positions.end.line + 1])


@dataclass
class PyrightDiagnostic:
    severity: PyrightSeverityLevel
    message: str
    file: str | None = None
    uri: PyrightUri | None = None
    range: PyrightRange | None = None
    rule: str | None = None

    def extract_path(self) -> Path:
        if self.uri is not None:
            return Path(self.uri._filePath)
        elif self.file is not None:
            return Path(self.file)
        else:
            raise ValueError("BUG! no URI, no file?")

    def __init__(
        self,
        file: str | None = None,
        uri: dict[str, str] | None = None,
        range: dict[str, dict[str, int]] | None = None,
        **kw,
    ):
        assert file is not None or uri is not None

        self.file = file
        if uri is not None:
            self.uri = PyrightUri(**uri)
        else:
            self.uri = None

        if range is not None:
            self.range = PyrightRange(**range)
        else:
            self.range = None

        for n, v in kw.items():
            setattr(self, n, v)

    def maybe_gitlab_report_location(
        self, abs_base_path
    ) -> GitlabReportLocation | None:
        if self.range is not None:
            return GitlabReportLocation(
                path=str(self.extract_path().resolve().relative_to(abs_base_path)),
                positions=self.range.to_positions(),
            )


@dataclass
class PyrightReport:
    version: str
    time: str
    generalDiagnostics: list[PyrightDiagnostic]
    summary: dict[str, int]

    @classmethod
    def from_json_file(cls, f: typing.TextIO) -> "PyrightReport":
        return cls(**json.load(f))

    def __init__(self, generalDiagnostics: list[dict[str, Any]], **kw):
        self.generalDiagnostics = [PyrightDiagnostic(**o) for o in generalDiagnostics]
        for n, v in kw.items():
            setattr(self, n, v)


class ReportFingerprint(str):
    pass


@dataclass
class GitlabReport:
    description: str
    fingerprint: ReportFingerprint
    severity: GitlabSeverityLevel
    location: GitlabReportLocation


def fingerprint(
    base_path: Path, description: str, location: GitlabReportLocation
) -> ReportFingerprint:
    return ReportFingerprint(
        md5(
            b"\0".join((description.encode(), location.get_lines(base_path).encode())),
            usedforsecurity=False,
        ).hexdigest()
    )


@dataclass
class GitlabIncompleteReport:
    """
    Report info without the location and fingerprinting
    """

    description: str
    severity: GitlabSeverityLevel

    def complete(self, base_path: Path, location: GitlabReportLocation) -> GitlabReport:
        return GitlabReport(
            description=self.description,
            severity=self.severity,
            location=location,
            fingerprint=fingerprint(base_path, self.description, location),
        )


def load_json(fname: str) -> PyrightReport:
    with open(fname, "rt") as f:
        return PyrightReport.from_json_file(f)


def convert_diagnostic_category_to_gitlab_severity(
    category: PyrightSeverityLevel,
) -> GitlabSeverityLevel:
    match category:
        case PyrightSeverityLevel.error:
            return GitlabSeverityLevel.blocker
        case PyrightSeverityLevel.warning:
            return GitlabSeverityLevel.major
        case PyrightSeverityLevel.unreachablecode:
            return GitlabSeverityLevel.major
        case PyrightSeverityLevel.deprecated:
            return GitlabSeverityLevel.minor
        case _:
            return GitlabSeverityLevel.info


def main():
    ap = ArgumentParser()
    ap.add_argument("--src", type=load_json)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--base-path", default=Path("."), type=Path)
    args = ap.parse_args()

    report = (
        args.src if args.src is not None else PyrightReport.from_json_file(sys.stdin)
    )

    if args.output is not None:
        args.output.parent.mkdir(exist_ok=True, parents=True)

    fout = open(args.output, "wt") if args.output is not None else sys.stdout

    response: list[GitlabReport] = []

    abs_base_path = args.base_path.resolve()

    for diag in report.generalDiagnostics:
        loc = diag.maybe_gitlab_report_location(abs_base_path)
        if loc is not None:
            response.append(
                GitlabIncompleteReport(
                    description=diag.message,
                    severity=convert_diagnostic_category_to_gitlab_severity(
                        diag.severity
                    ),
                ).complete(
                    base_path=abs_base_path,
                    location=loc,
                )
            )
        else:
            warnings.warn("some pyright reports thrown away because they had no range")

    print(json.dumps(list(asdict(r) for r in response)), file=fout)


if __name__ == "__main__":  # pragma: no cover
    main()
