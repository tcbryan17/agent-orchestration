"""Markdown table builder: the writer's tool for presenting comparisons.

WHY a tool and not free text: a validated table can't silently drop a cell, so the writer
can't misalign a comparison.
"""


def build_table(columns: list[str], rows: list[list[str]]) -> str:
    """Return a markdown table; raise ValueError if any row's width differs from `columns`."""
    if not columns:
        raise ValueError("a table needs at least one column")
    for i, row in enumerate(rows):
        if len(row) != len(columns):
            raise ValueError(f"row {i} has {len(row)} cells, expected {len(columns)}")

    def line(cells: list[str]) -> str:
        return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"

    header = [line(columns), "| " + " | ".join("---" for _ in columns) + " |"]
    return "\n".join(header + [line(r) for r in rows])
