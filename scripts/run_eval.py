"""Run the eval suite from the command line.

`--dry-run` only lists the tasks and never touches the API. A real run needs the systems
wired in (the multi-agent system and the single-agent baseline), which exist after Phases
2-5; until then this script refuses to run for real rather than pretending.
"""

import argparse
import sys
from decimal import Decimal
from pathlib import Path

from agent_orchestration.evals.runner import load_tasks

TASKS_DIR = Path(__file__).resolve().parents[1] / "evals" / "tasks"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="list tasks; no API calls")
    parser.add_argument("--max-usd", type=Decimal, default=Decimal("2"), help="dollar cap")
    parser.add_argument("--tasks-dir", type=Path, default=TASKS_DIR)
    args = parser.parse_args(argv)

    tasks = load_tasks(args.tasks_dir)
    if args.dry_run:
        print(f"{len(tasks)} tasks in {args.tasks_dir} (cap would be ${args.max_usd})")
        for t in tasks:
            print(f"  {t.id}  [{t.tier}]  {t.prompt}")
        return 0

    print(
        "Real runs need the multi-agent system and the baseline wired in (after Phases 2-5) "
        "and the C12 rubric written. Nothing was run.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
