from typing import List, Dict, Optional
from ..common.errors import QuoteScriptError
from ..common.models import FilterNode, SelectionNode, ProgramNode


TAG_ALIASES = {
    "forgiving": "forgiving",
    "f": "forgiving",
    "-forgiving": "forgiving",
    "-f": "forgiving",
    "exact": "exact",
    "e": "exact",
    "-exact": "exact",
    "-e": "exact",
    "loose": "loose",
    "l": "loose",
    "-loose": "loose",
    "-l": "loose",
}


def _is_string(tok: Optional[str]) -> bool:
    return bool(tok) and len(tok) >= 2 and tok[0] == '"' and tok[-1] == '"'


def _is_int(tok: Optional[str]) -> bool:
    return bool(tok) and tok.isdigit()


def _is_tag(tok: Optional[str]) -> bool:
    return bool(tok) and tok.lower() in TAG_ALIASES


def _canonical_tag(tok: str) -> str:
    return TAG_ALIASES[tok.lower()]


def parse(tokens: List[str]) -> ProgramNode:
    """Phase 2: Syntax analysis.

    Enforces:
    - ABOVE must appear before BELOW.
    - QUOTE, AUTHOR, THEME may each appear at most once.
    - Global order: QUOTE < AUTHOR < THEME.
    - BELOW may contain TOP, RANDOM, or both (TOP then RANDOM).

    BELOW keywords accepted:
    - TOP:
    - RANDOM:   (preferred)
    - RANDOM    (still accepted for backwards compatibility)
    """
    i = 0
    n = len(tokens)

    filters: Dict[str, FilterNode] = {}
    selection = SelectionNode(top=None, random=None)
    seen_top = False
    seen_random = False
    seen_below = False

    # order indices: QUOTE < AUTHOR < THEME
    order_index = {"quote": 0, "author": 1, "theme": 2}
    last_order = -1

    def peek(offset: int = 0) -> Optional[str]:
        idx = i + offset
        return tokens[idx] if 0 <= idx < n else None

    def consume() -> str:
        nonlocal i
        if i >= n:
            raise QuoteScriptError("Unexpected end of input")
        tok = tokens[i]
        i += 1
        return tok

    def skip_newlines():
        nonlocal i
        while i < n and tokens[i] == '\n':
            i += 1

    skip_newlines()

    while i < n:
        tok = peek()
        if tok == '\n':
            skip_newlines()
            continue

        # ABOVE: QUOTE / AUTHOR / THEME
        if tok in ("QUOTE:", "AUTHOR:", "THEME:"):
            if seen_below:
                raise QuoteScriptError(
                    "ABOVE (QUOTE/AUTHOR/THEME) cannot appear after BELOW (TOP/RANDOM)"
                )

            if tok == "QUOTE:":
                kind = "quote"
            elif tok == "AUTHOR:":
                kind = "author"
            else:
                kind = "theme"

            if kind in filters:
                raise QuoteScriptError(f"{kind.upper()} specified more than once")

            # enforce global order QUOTE < AUTHOR < THEME
            idx = order_index[kind]
            if idx < last_order:
                raise QuoteScriptError(
                    f"Invalid order: {kind.upper()} appears after a later field"
                )
            last_order = idx

            consume()  # keyword
            skip_newlines()
            val_tok = consume()
            if not _is_string(val_tok):
                raise QuoteScriptError(
                    f"Expected string literal after {kind.upper()}:, got {val_tok!r}"
                )
            value = val_tok[1:-1]  # strip quotes

            skip_newlines()
            next_tok = peek()
            tag = None
            if _is_tag(next_tok):
                tag = _canonical_tag(consume())

            # Expect newline or EOF
            if peek() == '\n':
                consume()

            filters[kind] = FilterNode(kind=kind, value=value, tag=tag)
            skip_newlines()
            continue

        # BELOW: TOP:
        if tok == "TOP:":
            seen_below = True
            if seen_top:
                raise QuoteScriptError("TOP specified more than once")
            consume()  # 'TOP:'
            skip_newlines()
            count_tok = consume()
            if not _is_int(count_tok):
                raise QuoteScriptError(f"Expected integer after TOP:, got {count_tok!r}")
            selection.top = int(count_tok)
            seen_top = True
            if peek() == '\n':
                consume()
            skip_newlines()
            continue

        # BELOW: RANDOM / RANDOM:
        # Accept:
        #   RANDOM: 2
        #   RANDOM 2    (legacy)
        #   RANDOM : 2  (forgiving)
        if tok in ("RANDOM", "RANDOM:"):
            seen_below = True
            if seen_random:
                raise QuoteScriptError("RANDOM specified more than once")

            consume()  # 'RANDOM' or 'RANDOM:'

            # Forgiving form: RANDOM : 2  (lexer would tokenize ':' separately)
            if tok == "RANDOM" and peek() == ":":
                consume()  # ':'

            skip_newlines()
            count_tok = consume()
            if not _is_int(count_tok):
                # tailor error message depending on style used
                raise QuoteScriptError(
                    f"Expected integer after RANDOM:, got {count_tok!r}"
                    if tok != "RANDOM"
                    else f"Expected integer after RANDOM, got {count_tok!r}"
                )

            selection.random = int(count_tok)
            seen_random = True

            if peek() == '\n':
                consume()
            skip_newlines()
            continue

        raise QuoteScriptError(f"Unexpected token {tok!r} at position {i}")

    if not filters and selection.top is None and selection.random is None:
        raise QuoteScriptError("Empty QuoteScript program")

    return ProgramNode(filters=filters, selection=selection)
