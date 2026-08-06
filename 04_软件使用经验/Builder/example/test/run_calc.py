#!/usr/bin/env python3
"""Run the calc.exe reverse-Polish calculator with sample inputs and print results."""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EXE = os.path.join(ROOT, "out", "calc.exe")
INPUT = os.path.join(HERE, "input.txt")

SAMPLE_INPUT = b"1 2 +\n3 4 *\n5 6 /\n10 5 -\n"


def main():
    if not os.path.exists(EXE):
        sys.exit(f"error: executable not found at {EXE} (run `make` first)")

    with open(INPUT, "wb") as f:
        f.write(SAMPLE_INPUT)

    with open(INPUT, "rb") as f:
        result = subprocess.run([EXE], stdin=f, capture_output=True, timeout=5)

    print("=== input ===")
    print(SAMPLE_INPUT.decode().rstrip())
    print("=== output ===")
    sys.stdout.write(result.stdout.decode("utf-8", errors="replace"))
    print("=== stderr ===")
    sys.stdout.write(result.stderr.decode("utf-8", errors="replace"))
    print(f"=== exit code: {result.returncode} ===")


if __name__ == "__main__":
    main()