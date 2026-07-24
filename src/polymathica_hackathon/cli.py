"""Command-line entry point for the hackathon workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from .workflow import DEFAULT_OUTPUT_DIR, run_workflow


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the POLYMATHICA hackathon evidence workflow.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR), help="Directory for generated evidence.")
    args = parser.parse_args()

    result = run_workflow(Path(args.output))
    print(f"Workflow: {result.workflow_id}")
    print(f"Validation: {result.validation_status}")
    print(f"Report: {result.report_path}")
    print(f"Archive: {result.archive_manifest_path}")
    return 0 if result.validation_status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
