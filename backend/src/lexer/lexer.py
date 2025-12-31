from typing import List
from ..common.errors import QuoteScriptError


def lex(source: str) -> List[str]:
    """Phase 1: Lexical analysis.

    Converts the raw QuoteScript source into a flat list of tokens:
    - keywords: QUOTE:, AUTHOR:, THEME:, TOP:, RANDOM, RANDOM:
    - string literals: "..." (including spaces inside)
    - identifiers / tags: forgiving, exact, loose, f, -f, etc.
    - integers: 0, 1, 2, ...
    - newline markers: '\n'
    """
    tokens: List[str] = []
    word = ""
    in_string = False
    i = 0
    n = len(source)

    while i < n:
        ch = source[i]

        if in_string:
            word += ch
            if ch == '"':
                # end of string literal
                tokens.append(word)
                word = ""
                in_string = False
            i += 1
            continue

        # Not inside a string
        if ch == '"':
            if word:
                tokens.append(word)
                word = ""
            in_string = True
            word = '"'
            i += 1
            continue

        if ch == '\n':
            if word.strip():
                tokens.append(word.strip())
                word = ""
            tokens.append('\n')
            i += 1
            continue

        if ch.isspace():  # space, tab, etc. (not newline)
            if word:
                tokens.append(word)
                word = ""
            i += 1
            continue

        word += ch
        i += 1

    if in_string:
        raise QuoteScriptError("Unterminated string literal")

    if word.strip():
        tokens.append(word.strip())

    return tokens
