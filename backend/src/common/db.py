
import sqlite3
from pathlib import Path
from typing import List, Dict, Any


def get_db_path() -> Path:
    # src/common/db.py -> src/common -> src -> root -> data/db/quotes.db
    return Path(__file__).resolve().parents[2] / "data" / "db" / "quotes.db"


def load_quotes() -> List[Dict[str, Any]]:
    """Load all quotes from the SQLite DB into memory as a list of dicts.

    Returns rows in rowid order so that TOP behaves like 'first N by insertion'.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT rowid AS _rowid, id, content, author, tags FROM quotes ORDER BY rowid;")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
