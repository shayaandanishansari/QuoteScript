import os
import sys
import sqlite3
from pathlib import Path
from typing import List, Dict, Any

from .errors import QuoteScriptError


_DB_REL = Path("data") / "db" / "quotes.db"


def _base_dir() -> Path:
    """
    Returns the directory that should contain `data/`.

    - Source mode: backend/ (derived from this file path)
    - Frozen (PyInstaller): folder containing the executable (sys.executable)
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    # backend/src/common/db.py -> backend/
    return Path(__file__).resolve().parents[2]


def get_db_path() -> Path:
    """
    Resolve the SQLite DB path.

    Priority:
      1) QUOTESCRIPT_DB_PATH (absolute path to .db)
      2) QUOTESCRIPT_DATA_DIR (path to `data/` directory)
      3) <base>/data/db/quotes.db
      4) PyInstaller one-file extraction dir (sys._MEIPASS)/data/db/quotes.db
    """
    env_db = os.getenv("QUOTESCRIPT_DB_PATH")
    if env_db:
        return Path(env_db).expanduser().resolve()

    env_data_dir = os.getenv("QUOTESCRIPT_DATA_DIR")
    if env_data_dir:
        return (Path(env_data_dir).expanduser().resolve() / "db" / "quotes.db")

    base = _base_dir()
    candidate = base / _DB_REL
    if candidate.exists():
        return candidate

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidate2 = Path(meipass) / _DB_REL
        if candidate2.exists():
            return candidate2

    # Return the most sensible default; caller will raise a clean error.
    return candidate


def load_quotes() -> List[Dict[str, Any]]:
    """Load all quotes from the SQLite DB into memory as a list of dicts.

    Returns rows in rowid order so that TOP behaves like 'first N by insertion'.
    """
    db_path = get_db_path()

    if not db_path.exists():
        raise QuoteScriptError(
            "QuoteScript DB not found.\n"
            f"Looked for: {db_path}\n"
            f"QUOTESCRIPT_DB_PATH={os.getenv('QUOTESCRIPT_DB_PATH')!r}\n"
            f"QUOTESCRIPT_DATA_DIR={os.getenv('QUOTESCRIPT_DATA_DIR')!r}\n"
            "Fix: ship `data/db/quotes.db` next to the executable, OR set QUOTESCRIPT_DB_PATH."
        )

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT rowid AS _rowid, id, content, author, tags "
        "FROM quotes ORDER BY rowid;"
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
