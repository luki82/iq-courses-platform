"""
Turn a lesson's plain-text content into structured blocks for display.

Lessons are written as plain text with a simple layout (see the seed
commands), for example:

    GOAL: Say hello, give your name and ask someone's name.

    KEY WORDS
    - Hello / Hi

    DIALOGUE
    Anna: Hi! My name is Anna.

    PRACTICE
    Complete the sentences.
    1. Hello, my name ___ Lina.

    ANSWERS: 1. is

parse_lesson() reads that layout and returns a list of blocks. A PRACTICE
section whose numbered items each have one blank (___), with a matching
numbered ANSWERS line, becomes an interactive drag-and-drop exercise; any
other practice is shown as text with the answers hidden behind a button.
Content that doesn't follow the layout still displays, as plain paragraphs.
"""

import random
import re
from dataclasses import dataclass, field

BLANK = "___"

# A heading is a line whose start (before any colon) is in capitals, with at
# least one word of two or more capital letters, e.g. "KEY WORDS", "A / AN",
# "GRAMMAR TIP: ...". "A B C D" (the alphabet) and "Anna: Hi!" are not headings.
HEADING_RE = re.compile(r"""^([A-Z][A-Z0-9 '&/()"\-]*?)\s*(?::\s*(.*))?$""")
HAS_CAPS_WORD_RE = re.compile(r"[A-Z]{2}")
BULLET_RE = re.compile(r"^[-•*]\s+(.*)$")
NUMBERED_LINE_RE = re.compile(r"^\d+[.)]\s+")
# Splits "1. foo  2. bar" into numbered parts. Requires a space after the
# dot so prices ($3.90) and times (9:30) aren't mistaken for item numbers.
NUMBER_SPLIT_RE = re.compile(r"(?:^|\s)(\d+)[.)]\s+")
SPEAKER_RE = re.compile(r"^([A-Z][A-Za-z']*(?: [A-Za-z']+){0,2}):\s+(.+)$")
TRAILING_NOTE_RE = re.compile(r"\s*\([^)]*\)\s*$")

DIALOGUE_SECTIONS = ("DIALOGUE", "CONVERSATION", "ROLE PLAY", "ROLE-PLAY")
ANSWER_SECTIONS = ("ANSWERS", "ANSWER", "SAMPLE ANSWERS", "SAMPLE ANSWER")


@dataclass
class Section:
    title: str = ""
    subtitle: str = ""
    lines: list = field(default_factory=list)


def _split_heading(line: str):
    """Return (title, inline_text) if the line is a heading, else None."""
    match = HEADING_RE.match(line)
    if not match:
        return None
    title = match.group(1).strip()
    if not HAS_CAPS_WORD_RE.search(title) or any(c.islower() for c in title):
        return None
    return title, (match.group(2) or "").strip()


def _sections(content: str) -> list:
    sections = [Section()]
    for raw in content.replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        heading = _split_heading(line) if line else None
        if heading:
            title, inline = heading
            sections.append(Section(title=title, subtitle=inline))
        else:
            sections[-1].lines.append(line)
    return [s for s in sections if s.title or any(s.lines)]


def _base_title(title: str) -> str:
    """'DIALOGUE (on the bus)' -> 'DIALOGUE'."""
    return re.sub(r"\s*\(.*\)$", "", title).strip()


def _numbered_parts(text: str):
    """'Do this: 1. a  2. b' -> ('Do this:', ['a', 'b'])."""
    pieces = NUMBER_SPLIT_RE.split(text)
    intro = pieces[0].strip()
    numbers = pieces[1::2]
    items = [p.strip() for p in pieces[2::2]]
    expected = [str(n) for n in range(1, len(numbers) + 1)]
    if numbers != expected:
        return intro, None
    return intro, items


def _text_blocks(lines: list, dialogue: bool = False) -> list:
    """Group plain lines into paragraph, bullet, numbered and dialogue blocks."""
    blocks = []

    def current(kind):
        if blocks and blocks[-1]["type"] == kind:
            return blocks[-1]
        block = {"type": kind, "items": []}
        blocks.append(block)
        return block

    for line in lines:
        if not line:
            if blocks and blocks[-1]["type"] == "para":
                blocks.append({"type": "break"})
            continue
        bullet = BULLET_RE.match(line)
        speaker = SPEAKER_RE.match(line) if dialogue else None
        if bullet:
            current("list")["items"].append(bullet.group(1))
        elif speaker:
            current("dialogue")["items"].append(
                {"speaker": speaker.group(1), "text": speaker.group(2)}
            )
        elif dialogue and blocks and blocks[-1]["type"] == "dialogue":
            # A wrapped line continues the previous speaker's turn.
            blocks[-1]["items"][-1]["text"] += " " + line
        elif NUMBERED_LINE_RE.match(line):
            current("numbered")["items"].append(NUMBERED_LINE_RE.sub("", line, count=1))
        else:
            current("para")["items"].append(line)

    return [b for b in blocks if b["type"] != "break"]


def _build_exercise(practice: Section, answers: Section | None, seed: str):
    """Return an exercise block, or None if the practice isn't fill-in-the-blank."""
    if answers is None:
        return None
    practice_text = " ".join(line for line in practice.lines if line)
    if practice.subtitle:
        practice_text = f"{practice.subtitle} {practice_text}"
    instruction, items = _numbered_parts(practice_text)
    answer_text = " ".join([answers.subtitle] + [line for line in answers.lines if line])
    _, answer_items = _numbered_parts(answer_text)

    if not items or not answer_items or len(items) != len(answer_items):
        return None
    if any(item.count(BLANK) != 1 for item in items):
        return None

    answer_words = [TRAILING_NOTE_RE.sub("", a).strip() for a in answer_items]
    if any(not a or "/" in a or len(a) > 30 for a in answer_words):
        return None

    exercise_items = []
    for number, (item, answer) in enumerate(zip(items, answer_words), start=1):
        before, after = item.split(BLANK)
        exercise_items.append(
            {"number": number, "before": before.rstrip(), "after": after.lstrip(), "answer": answer}
        )

    # Shuffle the word bank so it isn't in answer order, but keep it the same
    # on every page load for a given lesson.
    bank = list(answer_words)
    random.Random(seed).shuffle(bank)
    if bank == answer_words and len(bank) > 1:
        bank = bank[1:] + bank[:1]

    return {
        "type": "exercise",
        "instruction": instruction,
        "items": exercise_items,
        "bank": bank,
        "answers": answers,
    }


def parse_lesson(content: str, seed: str = "") -> list:
    blocks = []
    sections = _sections(content or "")
    index = 0
    while index < len(sections):
        section = sections[index]
        base = _base_title(section.title)

        if base == "GOAL":
            blocks.append({"type": "goal", "text": " ".join([section.subtitle] + [l for l in section.lines if l])})
            index += 1
            continue

        if base.startswith("PRACTICE"):
            answers = None
            if index + 1 < len(sections) and _base_title(sections[index + 1].title) in ANSWER_SECTIONS:
                answers = sections[index + 1]
            exercise = _build_exercise(section, answers, seed)
            blocks.append({"type": "heading", "title": section.title, "subtitle": ""})
            if exercise:
                blocks.append(exercise)
                index += 2
                continue
            blocks.extend(_text_blocks(([section.subtitle] if section.subtitle else []) + section.lines))
            if answers is not None:
                lines = [l for l in [answers.subtitle] + answers.lines if l]
                blocks.append(
                    {"type": "answers", "title": answers.title.title(), "blocks": _text_blocks(lines)}
                )
                index += 1
            index += 1
            continue

        if section.title:
            blocks.append({"type": "heading", "title": section.title, "subtitle": section.subtitle})
        is_dialogue = base in DIALOGUE_SECTIONS
        blocks.extend(_text_blocks(section.lines, dialogue=is_dialogue))
        index += 1

    return blocks
