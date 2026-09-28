from __future__ import annotations

import re
from dataclasses import dataclass

COLLEGE_CODE = "KB"
COLLEGE_NAME = "NBKR Institute of Science & Technology"

BRANCH_CODES = {
    "A05": "Computer Science and Engineering",
    "04": "Electronics and Communication Engineering",
    "03": "Mechanical Engineering",
    "01": "Civil Engineering",
    "30": "Artificial Intelligence and Data Science",
}

ENTRY_TYPE_CODES = {
    "1": "Regular Entry",
    "5": "Lateral Entry",
}

ROLL_PATTERN = re.compile(r"^(\d{2})([A-Za-z]{2})([15])([A-Za-z]?\d{2})([A-Za-z]\d+)$")


@dataclass
class RollNumberResult:
    valid: bool
    error: str | None = None
    admission_year: int | None = None
    college_code: str | None = None
    college: str | None = None
    entry_type_code: str | None = None
    entry_type: str | None = None
    branch_code: str | None = None
    branch: str | None = None
    student_identifier: str | None = None

    def to_dict(self) -> dict:
        return {
            "valid": self.valid,
            "error": self.error,
            "admission_year": self.admission_year,
            "college_code": self.college_code,
            "college": self.college,
            "entry_type_code": self.entry_type_code,
            "entry_type": self.entry_type,
            "branch_code": self.branch_code,
            "branch": self.branch,
            "student_identifier": self.student_identifier,
        }


def parse_roll_number(roll_number: str) -> RollNumberResult:
    normalized = (roll_number or "").strip().upper()
    match = ROLL_PATTERN.fullmatch(normalized)
    if not match:
        return RollNumberResult(valid=False, error="Please enter a valid NBKRIST roll number.")

    year_two, college_code, entry_code, branch_code_raw, student_identifier = match.groups()

    if college_code != COLLEGE_CODE:
        return RollNumberResult(
            valid=False,
            error="Invalid college code. This application currently supports NBKRIST roll numbers.",
        )

    entry_type = ENTRY_TYPE_CODES.get(entry_code)
    if not entry_type:
        return RollNumberResult(valid=False, error="Invalid entry type in roll number.")

    branch_code = branch_code_raw.upper()
    branch = BRANCH_CODES.get(branch_code)
    if not branch:
        return RollNumberResult(valid=False, error="Unknown branch code. Please verify your roll number.")

    return RollNumberResult(
        valid=True,
        admission_year=2000 + int(year_two),
        college_code=college_code,
        college=COLLEGE_NAME,
        entry_type_code=entry_code,
        entry_type=entry_type,
        branch_code=branch_code,
        branch=branch,
        student_identifier=student_identifier,
    )
