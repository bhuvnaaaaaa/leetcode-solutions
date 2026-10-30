#!/usr/bin/env python3
"""Regenerate the solutions table in the top-level README.

Reads each problem folder's README.md (written by sync.py) and the git history,
then replaces everything between the BEGIN/END SOLUTIONS markers.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BEGIN = "<!-- BEGIN SOLUTIONS -->"
END = "<!-- END SOLUTIONS -->"

LANGS = {
    "cpp": "C++", "java": "Java", "py": "Python", "c": "C", "cs": "C#",
    "js": "JavaScript", "ts": "TypeScript", "php": "PHP", "swift": "Swift",
    "kt": "Kotlin", "dart": "Dart", "go": "Go", "rb": "Ruby",
    "scala": "Scala", "rs": "Rust", "rkt": "Racket", "erl": "Erlang",
    "ex": "Elixir", "sql": "SQL", "sh": "Bash",
}
TITLE_RE = re.compile(r"^# \[(\d+)\. (.+)\]\((.+?)\)", re.M)


def last_commit_date(folder):
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ad", "--date=short", "--", folder.name],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.strip()
    return out or "-"


def read_problem(folder):
    readme = folder / "README.md"
    if not readme.exists():
        return None
    text = readme.read_text(encoding="utf-8")
    m = TITLE_RE.search(text)
    if not m:
        return None
    num, title, url = m.group(1), m.group(2), m.group(3)

    diff = re.search(r"\*\*Difficulty:\*\*\s*(\w+)", text)
    topics = re.search(r"\*\*Topics:\*\*\s*(.+)", text)

    langs = sorted({
        LANGS.get(f.suffix.lstrip("."), f.suffix.lstrip(".").upper())
        for f in folder.iterdir()
        if f.is_file() and f.name != "README.md"
    })

    return {
        "num": int(num),
        "title": title,
        "url": url,
        "difficulty": diff.group(1) if diff else "-",
        "topics": (topics.group(1).strip() if topics else "-"),
        "langs": ", ".join(langs) or "-",
        "folder": folder.name,
        "solved": last_commit_date(folder),
    }


def build_table(problems):
    counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    for p in problems:
        if p["difficulty"] in counts:
            counts[p["difficulty"]] += 1

    lines = [
        BEGIN,
        f"**{len(problems)} problems solved** — "
        f"{counts['Easy']} easy, {counts['Medium']} medium, {counts['Hard']} hard.",
        "",
        "| # | Problem | Difficulty | Topics | Language | Last solved |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for p in problems:
        lines.append(
            f"| {p['num']} | [{p['title']}]({p['url']}) | {p['difficulty']} | "
            f"{p['topics']} | [{p['langs']}]({p['folder']}/) | {p['solved']} |"
        )
    lines += ["", END]
    return "\n".join(lines)


def main():
    folders = sorted(f for f in ROOT.iterdir() if f.is_dir() and re.match(r"\d{4}-", f.name))
    problems = [p for p in (read_problem(f) for f in folders) if p]
    problems.sort(key=lambda p: p["num"])

    text = README.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        raise SystemExit(f"README.md is missing the {BEGIN} / {END} markers.")

    start, end = text.index(BEGIN), text.index(END) + len(END)
    updated = text[:start] + build_table(problems) + text[end:]
    if updated != text:
        README.write_text(updated, encoding="utf-8")
        print(f"Index updated: {len(problems)} problems.")
    else:
        print(f"Index already current: {len(problems)} problems.")


if __name__ == "__main__":
    main()
