"""Export a recorded run to the portfolio site's replay file.

Input: a JSONL file with one `Event` (as JSON) per line, as a recorder sink would write.
Output: `replay/sample-run.json`, a list of `{t, who, text}` built by the existing
`replay.to_site_events`, so the format stays defined in one place.
"""

import argparse
import json
from pathlib import Path

from agent_orchestration.events import Event
from agent_orchestration.replay import to_site_events


def export(source: Path, dest: Path) -> int:
    """Convert `source` (JSONL of events) to `dest`. Returns the number of site entries."""
    events = [
        Event.model_validate_json(line)
        for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    site = to_site_events(events)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(site, indent=2) + "\n", encoding="utf-8")
    return len(site)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="JSONL file of events")
    parser.add_argument("--out", type=Path, default=Path("replay/sample-run.json"))
    args = parser.parse_args(argv)
    n = export(args.source, args.out)
    print(f"wrote {n} entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
