"""Loading prompts from files, with a content hash.

Why files, not strings in code: prompts change more often than logic, and a reviewer should
see a prompt change as its own diff. Why a hash: the run manifest records `sha256` per agent,
so "which prompt produced this run?" has an exact answer even if the file later changes
(NIST AI RMF MEASURE; ISO 42001 lifecycle records).
"""

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Prompt:
    text: str
    sha256: str


def load_prompt(path: Path) -> Prompt:
    """Read a prompt file as UTF-8 and hash its exact bytes."""
    data = path.read_bytes()
    return Prompt(text=data.decode("utf-8"), sha256=hashlib.sha256(data).hexdigest())
