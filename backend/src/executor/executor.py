
import json
import random
from typing import List, Dict, Any

from ..common.models import IR
from ..common.db import load_quotes
from ..common.matching import match_exact, match_forgiving, match_loose, parse_tags_field


def _field_value(row: Dict[str, Any], field: str) -> str:
    if field == "quote":
        return row.get("content", "")
    if field == "author":
        return row.get("author", "")
    if field == "theme":
        # For THEME we operate on the tags field
        return row.get("tags", "")
    return ""


def _match_text(text: str, value: str, tag: str) -> bool:
    if tag == "exact":
        return match_exact(text, value)
    if tag == "loose":
        return match_loose(text, value)
    # forgiving default
    return match_forgiving(text, value)


def _matches_filter(row: Dict[str, Any], field: str, value: str, tag: str) -> bool:
    text = _field_value(row, field)
    if field == "theme":
        # For THEME, treat tags as a list and match against each tag
        tags = parse_tags_field(text)
        return any(_match_text(t, value, tag) for t in tags)
    return _match_text(text, value, tag)


def execute(ir: IR) -> List[Dict[str, Any]]:
    """Phase 6: Execute IR over the SQLite quotes DB.

    Returns the final list of matching quote rows.
    """
    rows = load_quotes()

    # 1) Apply ABOVE filters (all combined with AND)
    filtered = []
    for row in rows:
        ok = True
        for f in ir.filters:
            if not _matches_filter(row, f.field, f.value, f.tag):
                ok = False
                break
        if ok:
            filtered.append(row)

    # 2) Apply BELOW selection (TOP / RANDOM)
    sel = ir.selection
    result = filtered

    # TOP first (respect DB order)
    if sel.top is not None:
        if sel.top < len(result):
            result = result[: sel.top]

    # Then RANDOM if requested
    if sel.random is not None:
        n = sel.random
        if n == 0:
            result = []
        else:
            # If RANDOM only (no TOP) and n > len(result), just cap at len(result)
            n = min(n, len(result))
            result = random.sample(result, n)

    return result


def print_output(ir: IR, rows: List[Dict[str, Any]]) -> None:
    """print("=== IR ===")
    ir_dict = {
        "filters": [
            {"field": f.field, "value": f.value, "tag": f.tag}
            for f in ir.filters
        ],
        "selection": {"top": ir.selection.top, "random": ir.selection.random},
    }
    print(json.dumps(ir_dict, indent=2))"""

    # print("\nResults")
    if not rows:
        print("No matches found.")
        return

    for row in rows:
        print(f"- {row['content']} — {row['author']}  [tags={row['tags']}]")
