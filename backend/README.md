
# QuoteScript – Mini Compiler & Executor (Assignment Build)

This project implements the assignment version of **QuoteScript**, a small DSL
for querying a quotes database.

The focus here is on:
- A clear, regular grammar
- Classic compiler phases (lexing → parsing → semantic analysis → IR → optimisation → execution)
- A working end‑to‑end implementation over a SQLite database

## Project Structure

```text
QuoteScript/
  data/
    db/
      quotes.db        # SQLite database of quotes
    models/            # (reserved for future dataset/model artefacts)
  src/
    common/            # Shared models, matching logic, DB access
    lexer/             # Phase 1 – lexical analysis
    parser/            # Phase 2 – syntax analysis
    semantic/          # Phase 3 – semantic analysis
    ir/                # Phase 4 – IR generation
    optimizer/         # Phase 5 – optimisation
    executor/          # Phase 6 – execution over the DB
  main.py              # CLI entry point
```

## Grammar (v1 – Assignment)

```text
S   -> ST

ST  -> ABOVE BELOW
     | ABOVE
     | BELOW

ABOVE -> quote author theme
      |  quote author
      |  quote theme
      |  author theme
      |  quote
      |  author
      |  theme

BELOW -> top random
       | top
       | random

quote  -> "QUOTE:"  STR  TAG "/n"
author -> "AUTHOR:" STR  TAG "/n"
theme  -> "THEME:"  STR  TAG "/n"

top    -> "TOP:"    INT "/n"
random -> "RANDOM"  INT "/n"

TAG        -> forgiving | exact | loose
forgiving  -> "forgiving" | "f" | "-forgiving" | "-f"
exact      -> "exact"     | "e" | "-exact"     | "-e"
loose      -> "loose"     | "l" | "-loose"     | "-l"

INT -> "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | INT

STR -> "CHAR" | STR
```

Practical interpretations used by the implementation:

- `STR` is any double‑quoted string, e.g. `"Truth Knowledge"`.
- `INT` is one or more digits (`[0-9]+`), including `0`.
- `TAG` is optional in practice; when omitted it defaults to **forgiving**.

Valid ABOVE combinations (respecting global order QUOTE < AUTHOR < THEME):

- `quote`
- `author`
- `theme`
- `quote author`
- `quote theme`
- `author theme`
- `quote author theme`

BELOW may be:

- only `TOP: M`
- only `RANDOM N`
- `TOP: M` followed by `RANDOM N` (“RANDOM N out of TOP M”, with `0 ≤ N ≤ M`)

## Running

From the project root:

```bash
python main.py examples/example1.qs
```

Or create a new `.qs` file and point `main.py` to it.

The program will:

1. Lex and parse the QuoteScript source.
2. Perform semantic checks and defaults.
3. Generate a JSON‑like IR.
4. Optimise it lightly.
5. Execute the query over `data/db/quotes.db`.
6. Print the IR and the matching quotes (or "No matches found.").

This build is intentionally strict and grammar‑driven for the assignment.
A future v2 can relax ordering and evolve matching semantics based on user feedback.
