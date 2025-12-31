
from ..common.models import ProgramNode
from ..common.errors import QuoteScriptError


def semantic_analysis(program: ProgramNode) -> ProgramNode:
    """Phase 3: Semantic analysis.

    - Default TAG = 'forgiving' when omitted.
    - Validate TAG values.
    - Allow INT = 0.
    - If both TOP and RANDOM present, enforce 0 <= RANDOM <= TOP.
    """
    # Fill tag defaults & validate
    for name, flt in program.filters.items():
        if not flt.value:
            raise QuoteScriptError(f"Empty value for {name} filter")
        if flt.tag is None:
            flt.tag = "forgiving"
        if flt.tag not in ("exact", "forgiving", "loose"):
            raise QuoteScriptError(f"Invalid tag {flt.tag!r} for {name}")

    sel = program.selection

    # If both present: RANDOM N out of TOP M with 0 <= N <= M
    if sel.top is not None and sel.random is not None:
        if sel.random < 0 or sel.top < 0:
            raise QuoteScriptError("TOP and RANDOM counts cannot be negative")
        if sel.random > sel.top:
            raise QuoteScriptError("RANDOM count cannot exceed TOP count (N <= M required)")

    # If only one present, INT can be any >= 0 (0 allowed => zero results)
    if sel.top is not None and sel.top < 0:
        raise QuoteScriptError("TOP count cannot be negative")
    if sel.random is not None and sel.random < 0:
        raise QuoteScriptError("RANDOM count cannot be negative")

    return program
