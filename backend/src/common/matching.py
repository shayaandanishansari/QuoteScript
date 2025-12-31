
import re
import difflib
import ast
from typing import List


def _normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _normalize_case_and_spaces(s: str) -> str:
    return _normalize_spaces(s).lower()


def match_exact(field: str, query: str) -> bool:
    """Exact matching: whole word(s), case-sensitive, character-precise.

    Uses word boundaries so 'Freedom' does not match 'Freedoms'.
    """
    field = field or ""
    query = query or ""
    pattern = r"\b" + re.escape(query) + r"\b"
    return re.search(pattern, field) is not None


def _similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def match_forgiving(field: str, query: str) -> bool:
    """Forgiving matching: case-insensitive, tolerant of spacing and small misspellings."""
    if not field or not query:
        return False

    field_norm = _normalize_case_and_spaces(field)
    query_norm = _normalize_case_and_spaces(query)

    # Direct substring first
    if query_norm in field_norm:
        return True

    # Then approximate per-word similarity
    for word in field_norm.split():
        if _similar(word, query_norm) >= 0.8:
            return True
    return False


def _stem(word: str) -> str:
    """Very naive stemming for LOOSE matching."""
    w = word.lower()
    for suf in ("ing", "ed", "es", "s"):
        if len(w) > 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def match_loose(field: str, query: str) -> bool:
    """Loose matching: forgiving plus basic morphology (same root, etc.)."""
    if not field or not query:
        return False

    field_norm = _normalize_case_and_spaces(field)
    query_norm = _normalize_case_and_spaces(query)

    # Forgiving baseline
    if query_norm in field_norm:
        return True

    field_words = field_norm.split()
    query_words = query_norm.split()
    stems = {_stem(w) for w in query_words if w}

    for fw in field_words:
        fw_norm = fw.lower()
        for st in stems:
            if st and (fw_norm.startswith(st) or _similar(fw_norm, st) >= 0.8):
                return True
    return False


def parse_tags_field(raw: str) -> List[str]:
    """Parse the tags TEXT field from the DB.

    The CSV/DB stores tags like: "['Famous Quotes', 'Wisdom']".
    We try to interpret this as a Python list; if that fails, we fall back to a
    single-element list containing the raw string.
    """
    if not raw:
        return []
    try:
        value = ast.literal_eval(raw)
        if isinstance(value, list):
            return [str(x) for x in value]
        return [str(value)]
    except Exception:
        return [raw]
