#!/usr/bin/env python3
"""Test suite for the calc reverse-Polish calculator."""

import os
import subprocess
import sys
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXE = os.path.join(ROOT, "out", "calc.exe" if os.name == "nt" else "calc")


@dataclass
class Case:
    name: str
    input: bytes
    expected_stdout: bytes
    expected_stderr: bytes = b""
    expected_rc: int = 0


CASES = [
    Case("basic +", b"1 2 +\n", b"\t3\n"),
    Case("basic -", b"10 5 -\n", b"\t5\n"),
    Case("basic *", b"3 4 *\n", b"\t12\n"),
    Case("basic /", b"10 4 /\n", b"\t2.5\n"),
    Case("chained", b"1 2 + 3 4 - * 5 /\n", b"\t-0.6\n"),
    Case("multi-line", b"1 2 +\n3 4 *\n5 6 /\n10 5 -\n",
         b"\t3\n\t12\n\t0.83333333\n\t5\n"),
    Case("float", b"3.14 2 *\n", b"\t6.28\n"),
    Case("divide by zero", b"1 0 /", b"error: zero divisor\n", b""),
    Case("stack underflow", b"+", b"error: stack empty\nerror: stack empty\n", b""),
]


def run_case(case: Case) -> tuple[bool, str]:
    if not os.path.exists(EXE):
        return False, f"executable not found: {EXE} (run `make` first)"

    r = subprocess.run([EXE], input=case.input, capture_output=True, timeout=5)

    def norm(b: bytes) -> bytes:
        return b.replace(b"\r\n", b"\n")

    actual = (norm(r.stdout), norm(r.stderr), r.returncode)
    expected = (norm(case.expected_stdout), norm(case.expected_stderr), case.expected_rc)

    if actual == expected:
        return True, ""

    lines = [f"  stdout: got {r.stdout!r}, want {case.expected_stdout!r}"]
    if norm(r.stderr) != norm(case.expected_stderr):
        lines.append(f"  stderr: got {r.stderr!r}, want {case.expected_stderr!r}")
    if r.returncode != case.expected_rc:
        lines.append(f"  rc:     got {r.returncode}, want {case.expected_rc}")
    return False, "\n".join(lines)


def main() -> int:
    passed = failed = 0
    print(f"Running {len(CASES)} test cases against {EXE}\n")
    for case in CASES:
        ok, detail = run_case(case)
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {case.name}")
        if not ok:
            print(detail)
            failed += 1
        else:
            passed += 1

    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())