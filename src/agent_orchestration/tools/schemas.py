"""Tool schemas: what the model is told about each tool (C3).

Once you write `edgar_schema()`, the calculator and table schemas follow the same pattern and
can be written by agents.
"""

from anthropic.types import ToolParam


def edgar_schema() -> ToolParam:
    """TODO(human) C3: write the schema the model sees for the EDGAR facts tool.

    The schema and description are a prompt: the model reads them to decide when and how to
    call the tool, so how tight you make them shapes both errors and flexibility.

      A. Enums for company and XBRL concept: far fewer invalid calls, but you must update
         the enum whenever a company or concept is added.
      B. Free strings: flexible, but the model invents CIKs and concept names.
      C. `strict: true` (guaranteed schema-conformant input) vs a loose schema you
         validate yourself in dispatch (C2).
      D. Description wording: say what it returns, units, and when NOT to use it (for
         example, "not for club accounts").

    The schema must require the company field.

    Guide: docs/concepts/c03-tool-schema.md
    Governance: NIST AI RMF MANAGE; OWASP LLM excessive agency (narrow tools, narrow inputs).
    """
    raise NotImplementedError("C3: see docs/concepts/c03-tool-schema.md")
