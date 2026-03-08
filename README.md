# QuoteScript

QuoteScript is a domain-specific language (DSL) for querying and exploring a quotes database, paired with a desktop GUI for writing and running scripts interactively.

## What is it?

QuoteScript lets you express what you want from a quotes collection in a clean, human-readable syntax — and get back exactly that. The runtime is a Python interpreter for the DSL; the interface is a Flutter desktop app that invokes Python each time a script is run.

```
QUOTE: "Freedom"
TOP: 10
```

That's it. Run the script, get your quotes — filtered, ranked, tagged.

## How to Use

1. Open the QuoteScript Runner desktop app
2. Write your QuoteScript query in the left panel
3. Hit **Run**
4. View results (stdout / IR + results) and any errors in the right panel

## DSL Reference

| Keyword | Description | Example |
|---|---|---|
| `QUOTE:` | Filter quotes by keyword or topic | `QUOTE: "Freedom"` |
| `TOP:` | Limit results to the top N | `TOP: 10` |

*(More keywords may be added as the language evolves.)*

## How it Works

QuoteScript is split into two layers:

- **DSL Interpreter (Python)** — Parses and executes `.qs` scripts against the quotes database. Each run invokes `python.exe` fresh, keeping execution stateless and predictable.
- **Flutter Desktop GUI** — A split-pane interface: script editor on the left, output panel on the right. Tabs separate clean output (`Stdout / IR + Results`) from runtime errors (`Errors (stderr)`).

The quotes database is sourced from [Luke Peavy's quotable-io/data](https://github.com/quotable-io/data) — a well-curated, structured collection of quotes with authors and tags.

### Folder Structure

```
QuoteScript/
|---- interpreter/       (Python DSL runtime)
|---- data/              (quotes database)
|---- gui/               (Flutter desktop app)
|---- run.exe            (launcher)
```

## Why QuoteScript?

There is something to be said for having the right words at the right moment. Philosophers, leaders, poets — humanity has been distilling hard-won understanding into sentences for millennia. A well-asked question to that corpus is worth a great deal.

QuoteScript started as a practical tool: I wanted to query a quotes database without writing boilerplate search logic every time. A small DSL felt like the right abstraction — expressive enough to be useful, constrained enough to stay simple. The Flutter GUI made it feel like a real tool rather than a script you run in a terminal.

The deeper motivation was the same one behind projects like this generally: the belief that knowledge should be accessible, browsable, and queryable — not locked behind interfaces that don't let you ask the questions you actually have.

## Credits

- Quotes database: [Luke Peavy — quotable-io/data](https://github.com/quotable-io/data)
- DSL runtime: Python
- Desktop GUI: Flutter
