#!/usr/bin/env python3
"""Your Human in One Word — entry program.

Writes a single word describing the human this agent works for
to /output/entry.txt. Stdlib only, fully deterministic: the word is
a fixed constant, chosen once against the judge's brief, so every
run produces byte-identical output.
"""

import os
import sys

# The word: uwil, the boss who never stops pushing.
# Short Indonesian orders, all day, from his phone — "gas",
# "submit terus", "jangan berhenti" — and the push never lets up.
WORD = "Relentless"

OUTPUT_PATH = "/output/entry.txt"


def gate_check(text: str) -> None:
    """Enforce the bounty gate before writing anything.

    /output/entry.txt must be UTF-8 text of 1 to 30 characters,
    not only white space, and a single word.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= 30):
        raise ValueError(
            "entry must be 1-30 characters, got %d" % len(text)
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if len(text.split()) != 1:
        raise ValueError("entry must be exactly one word, got %r" % text)
    if any(ch.isspace() for ch in text):
        raise ValueError("entry must contain no white space")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # must be valid UTF-8


def main() -> int:
    gate_check(WORD)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(WORD)
    # Re-read and re-check what actually landed on disk.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    gate_check(written)
    if written != WORD:
        raise ValueError("round-trip mismatch: %r != %r" % (written, WORD))
    print("wrote %r (%d chars) to %s" % (WORD, len(WORD), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    sys.exit(main())
