
import sys
from src.pipeline import compile_and_run
from src.common.errors import QuoteScriptError


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <quotescript_file>")
        print("Example: python main.py examples/example1.qs")
        raise SystemExit(1)

    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
    except OSError as e:
        print(f"Error reading file {path!r}: {e}")
        raise SystemExit(1)

    try:
        compile_and_run(source)
    except QuoteScriptError as e:
        print("QuoteScript error:", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
