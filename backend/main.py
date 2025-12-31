import os
import sys
import argparse

from src.pipeline import compile_and_run
from src.common.errors import QuoteScriptError


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="quotescript_cli",
        description="QuoteScript CLI (compiler + executor)",
    )
    parser.add_argument(
        "quotescript_file",
        nargs="?",
        help="Path to a .qs file, or '-' to read from stdin",
    )
    parser.add_argument(
        "--db",
        dest="db_path",
        help="Path to quotes SQLite DB (overrides QUOTESCRIPT_DB_PATH)",
    )
    parser.add_argument(
        "--data-dir",
        dest="data_dir",
        help="Path to data/ directory (overrides QUOTESCRIPT_DATA_DIR)",
    )

    args = parser.parse_args()

    if args.db_path:
        os.environ["QUOTESCRIPT_DB_PATH"] = args.db_path
    if args.data_dir:
        os.environ["QUOTESCRIPT_DATA_DIR"] = args.data_dir

    if not args.quotescript_file:
        print("Usage: quotescript_cli <quotescript_file>", file=sys.stderr)
        print("Example: quotescript_cli examples/example1.qs", file=sys.stderr)
        raise SystemExit(1)

    path = args.quotescript_file

    try:
        if path == "-":
            source = sys.stdin.read()
        else:
            with open(path, "r", encoding="utf-8") as f:
                source = f.read()
    except OSError as e:
        print(f"Error reading file {path!r}: {e}", file=sys.stderr)
        raise SystemExit(1)

    try:
        compile_and_run(source)
    except QuoteScriptError as e:
        print("QuoteScript error:", e, file=sys.stderr)
        raise SystemExit(1)
    except Exception as e:
        print("Unexpected error:", e, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
