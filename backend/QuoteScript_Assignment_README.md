# QuoteScript Compiler Assignment – What To Draw & Write (By Hand)

This document explains **exactly** what needs to be written/drawn on paper to complete the compiler construction assignment for the QuoteScript project.

Use this **same example program** everywhere:

```text
QUOTE: "Freedom" exact
AUTHOR: "Epictetus" forgiving
THEME: "Wisdom" loose
TOP: 5
RANDOM 2
```

Meaning in English:

> Find quotes whose text contains “Freedom” (exact), whose author matches “Epictetus” (forgiving), and whose tags are loosely related to “Wisdom”. From the results, take the first 5 (TOP 5), then randomly choose 2 out of those.

---

## Page 1 – Title & Objective

**Write (no diagram):**

- Title (big):
  ```text
  QuoteScript – A Mini Compiler for a Quote Query Language
  ```
- Below it:
  - Student name + roll number  
  - Course: Compiler Construction  
  - Teacher's name  
  - Semester + Year

**Objective paragraph:**

```text
Objective:
The aim of this project is to design a small domain specific language (QuoteScript)
for querying a quotes database, and to implement a compiler pipeline for it:
lexical analysis, syntax analysis, semantic analysis, intermediate code generation,
optimisation and execution.
```

---

## Page 2 – Language Description & Example Program

**Heading:** `Language Description (QuoteScript)`

Write:

```text
QuoteScript is a small line-oriented query language that allows a user to
search a database of quotes. The user can specify filters on:

- QUOTE: the quote text
- AUTHOR: the author name
- THEME: the tags or theme of the quote

and then specify how many results to return using:

- TOP: take the first N results (in database order)
- RANDOM: randomly pick N results from the current set.

ABOVE = QUOTE / AUTHOR / THEME
BELOW = TOP / RANDOM

ABOVE must always come before BELOW.
```

**Valid ABOVE combinations (in order QUOTE → AUTHOR → THEME):**

```text
quote
author
theme
quote author
quote theme
author theme
quote author theme
```

**Example program (write this nicely boxed):**

```text
Example QuoteScript Program

QUOTE: "Freedom" exact
AUTHOR: "Epictetus" forgiving
THEME: "Wisdom" loose
TOP: 5
RANDOM 2
```

---

## Page 3 – Formal Grammar

**Heading:** `Formal Grammar of QuoteScript`

Write this grammar:

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

**Note under it:**

```text
Notes:
- In implementation, STR is any double-quoted string, e.g. "Truth Knowledge".
- INT is one or more digits (0–9), including 0.
- TAG is optional in the compiler implementation; if missing, it defaults to 'forgiving'.
```

---

## Page 4 – Tokens and Regular Expressions (Lexical Analysis)

**Heading:** `Lexical Analysis – Tokens and Patterns`

Draw a simple table:

| Token type | Examples                                      | Description / Pattern                     |
|-----------|-----------------------------------------------|-------------------------------------------|
| KEYWORD   | `QUOTE:`, `AUTHOR:`, `THEME:`, `TOP:`, `RANDOM` | Fixed strings                            |
| STRING    | `"Freedom"`, `"Wisdom Truth"`                 | `"[^"]*"` (characters inside quotes)      |
| INT       | `0`, `5`, `10`, `123`                         | `[0-9]+`                                  |
| TAG       | `exact`, `forgiving`, `loose`, `f`, `-f`, `e`, `-e`, `l`, `-l` | Recognised by keyword/alias list |
| NEWLINE   | end of line                                   | `\n`                                      |
| WHITESPACE| spaces, tabs                                  | ignored (outside strings)                 |

Under the table write:

```text
- The lexical analyser ignores whitespace outside string literals.
- Strings are read character by character from opening " to closing ".
- Keywords and tag aliases are recognised by comparing the full word.
```

---

## Page 5 – Lexical DFA + Tokenization Example

**Heading:** `Lexical DFA (Simplified)`

### A. DFA Diagram (simplified)

Draw 4–5 circles:

- `S` (start)
- `IN_STRING`
- `IN_INT`
- `DONE_WORD` (for identifiers/keywords)
- maybe a generic `ACCEPT` or just show arrows and notes

Transitions (you just need to show conceptually):

- From `S` on `"` → `IN_STRING`
- From `IN_STRING` on any char except `"` → loops in `IN_STRING`
- From `IN_STRING` on `"` → emit STRING token, go back to `S`
- From `S` on digit → `IN_INT`
- From `IN_INT` on digit → loops
- From `IN_INT` on non-digit → emit INT token, go back to `S`
- From `S` on letter / `:` → `DONE_WORD` (emit WORD/KEYWORD at boundary)
- From `S` on space/tab → stay in `S` (ignored)
- From `S` on newline → emit NEWLINE

You can annotate transitions with text like “emit token” next to them – doesn’t need to be perfect automata notation.

### B. Tokenization of the example

Write the program again:

```text
QUOTE: "Freedom" exact
AUTHOR: "Epictetus" forgiving
THEME: "Wisdom" loose
TOP: 5
RANDOM 2
```

Under it, list tokens:

```text
Tokens:

[QUOTE:, "Freedom", exact, \n,
 AUTHOR:, "Epictetus", forgiving, \n,
 THEME:, "Wisdom", loose, \n,
 TOP:, 5, \n,
 RANDOM, 2, \n]
```

---

## Page 6 – Syntax Analysis (Parse Tree / Derivation)

**Heading:** `Syntax Analysis – Parse Tree for the Example`

### A. Short derivation (informal)

```text
S
⇒ ST
⇒ ABOVE BELOW
⇒ quote author theme BELOW
⇒ "QUOTE:" STR TAG "/n" author theme BELOW
⇒ "QUOTE:" "Freedom" exact "/n" author theme BELOW
⇒ "QUOTE:" "Freedom" exact "/n"
   "AUTHOR:" "Epictetus" forgiving "/n"
   "THEME:" "Wisdom" loose "/n"
   BELOW
⇒ ABOVE top random
⇒ ABOVE TOP: 5 "/n" RANDOM 2 "/n"
```

This shows the high-level use of rules.

### B. Draw the parse tree

Draw a tree:

- Root: `S`
  - child: `ST`
    - children: `ABOVE` and `BELOW`

Under `ABOVE`, draw children `quote`, `author`, `theme`:

- `quote`
  - `QUOTE:`
  - `STR` → `"Freedom"`
  - `TAG` → `exact`
  - `/n`
- `author`
  - `AUTHOR:`
  - `STR` → `"Epictetus"`
  - `TAG` → `forgiving`
  - `/n`
- `theme`
  - `THEME:`
  - `STR` → `"Wisdom"`
  - `TAG` → `loose`
  - `/n`

Under `BELOW`, draw `top` and `random`:

- `top`
  - `TOP:`
  - `INT` → `5`
  - `/n`
- `random`
  - `RANDOM`
  - `INT` → `2`
  - `/n`

Make it neat – clear labels for non-terminals and terminals.

---

## Page 7 – Semantic Analysis Rules

**Heading:** `Semantic Analysis Rules`

Write bullet points:

```text
1. Tag defaulting:
   - If TAG is omitted after QUOTE/AUTHOR/THEME, default tag = 'forgiving'.

2. Tag validity:
   - Valid tags (or aliases): exact, forgiving, loose,
     and their aliases: f, -f, e, -e, l, -l.
   - Any other tag value causes a semantic error.

3. Filter uniqueness and order:
   - QUOTE, AUTHOR, THEME can appear at most once each.
   - Global order must be: QUOTE → AUTHOR → THEME.
   - ABOVE (filters) cannot appear after BELOW (TOP/RANDOM).

4. Selection validation:
   - TOP and RANDOM are optional.
   - If both are present: 0 ≤ RANDOM ≤ TOP.
   - INT values can be 0 (meaning zero results).

5. Non-empty program:
   - Program must have at least ABOVE or BELOW (or both).

6. Meaning of ABOVE and BELOW:
   - ABOVE = intersection (AND) of all filters.
   - BELOW:
     • TOP M → take first M rows (in database order).
     • RANDOM N → take N random rows from current set.
     • TOP M + RANDOM N → first TOP M, then RANDOM N out of those.
```

At the end, show **one semantic error example**:

```text
Example semantic error:

AUTHOR: "Epictetus"
QUOTE: "Freedom"

Error: AUTHOR appears before QUOTE (violates QUOTE → AUTHOR → THEME order).
```

---

## Page 8 – Intermediate Representation (IR)

**Heading:** `Intermediate Code / IR Design`

1. Describe IR shape:

```text
IR = {
  filters: [
    { field: "quote",  value: string, tag: "exact|forgiving|loose" },
    { field: "author", value: string, tag: "..." },
    { field: "theme",  value: string, tag: "..." }
  ],
  selection: {
    top:    integer or null,
    random: integer or null
  }
}
```

2. Draw a simple box diagram:

- Box labelled `IR`
  - Left small box: `filters` → arrows to 0–3 `Filter` boxes (`field`, `value`, `tag`)
  - Right small box: `selection` (`top`, `random`)

3. IR for the example program:

```text
filters = [
  { field: "quote",  value: "Freedom",   tag: "exact" },
  { field: "author", value: "Epictetus", tag: "forgiving" },
  { field: "theme",  value: "Wisdom",    tag: "loose" }
]

selection = { top: 5, random: 2 }
```

---

## Page 9 – Optimisation & Execution (Code Generation)

**Heading:** `Optimisation and Execution`

### A. Optimisation

Write:

```text
Optimisation (simple):

- Trim whitespace from filter values.
- Drop any filter whose value becomes completely empty.
- Normalise all tags to lowercase ('Exact' → 'exact').
```

Draw a small arrow:

```text
ProgramNode → IR → Optimiser → Optimised IR
```

### B. Execution (Code Generation)

Explain in words:

```text
Execution steps:

1. Load all rows from SQLite table:

   quotes(id TEXT, content TEXT, author TEXT, tags TEXT)

2. For each row:
   - QUOTE filter is matched against the 'content' column.
   - AUTHOR filter is matched against the 'author' column.
   - THEME filter is matched against each element in 'tags'.

3. Matching behaviour:
   - exact   → whole-word, case-sensitive match.
   - forgiving → case-insensitive, allows small typos.
   - loose   → forgiving + simple stemming (same word root).

4. If a row satisfies all filters, it is included in the result list.

5. Apply selection:
   - If TOP M is given, keep only first M rows.
   - If RANDOM N is given, pick N random rows from the current list.
   - If both TOP and RANDOM are given, first apply TOP M, then RANDOM N.
```

Also include very short pseudo-code:

```text
result = []
for each row in quotes:
    if row matches all filters:
        result.append(row)

if top is not None:
    result = first top rows

if random is not None:
    choose random rows from result
```

---

## Page 10 – Database Schema & Architecture Diagram

### A. Database Schema

**Heading:** `Database Schema`

Write:

```text
Table: quotes

Columns:
- id      TEXT PRIMARY KEY
- content TEXT NOT NULL   -- the quote text
- author  TEXT NOT NULL   -- author name
- tags    TEXT NOT NULL   -- e.g. "['Famous Quotes', 'Wisdom']"

THEME filters are matched against each tag inside the tags list.
```

### B. Overall System / Compiler Architecture

**Heading:** `Overall Compiler Architecture`

Draw a pipeline of boxes:

```text
QuoteScript Source
        ↓
      Lexer
        ↓
      Parser
        ↓
Semantic Analyzer
        ↓
    IR Generator
        ↓
      Optimizer
        ↓
      Executor
        ↓
  SQLite DB (quotes)
        ↓
   Printed Results
```

Label arrows if you like (tokens, AST, IR, etc.).

---

## Page 11 – Sample Run & Output

**Heading:** `Sample Run`

Write:

```text
Input program:

QUOTE: "Freedom" exact
AUTHOR: "Epictetus" forgiving
THEME: "Wisdom" loose
TOP: 5
RANDOM 2
```

**Example of printed IR (shortened):**

```text
IR:
{
  "filters": [
    { "field": "quote",  "value": "Freedom",   "tag": "exact" },
    { "field": "author", "value": "Epictetus", "tag": "forgiving" },
    { "field": "theme",  "value": "Wisdom",    "tag": "loose" }
  ],
  "selection": { "top": 5, "random": 2 }
}
```

**Example of results:**

If some row matches:

```text
Results:
- Freedom is the right to live as we wish. — Epictetus [tags=['Freedom']]
```

If nothing matches in your actual DB, then:

```text
Results:
No matches found.
```

Both are acceptable; the main point is to show what would be printed.

---

## Page 12 (Optional) – Future Work

**Heading:** `Future Work (QuoteScript v2)`

Write a few bullets:

```text
- Allow ABOVE fields (QUOTE, AUTHOR, THEME) in any order.
- Implement more advanced loose matching using NLP / word embeddings.
- Add sorting by popularity or date of the quotes.
- Build a GUI or web interface for writing and executing QuoteScript queries.
```

---

If you copy this structure onto paper (with diagrams where mentioned), you’ll have a complete, coherent compiler assignment for QuoteScript.
