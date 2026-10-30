#!/usr/bin/env python3
"""Sync accepted LeetCode submissions into this repo, one git commit per submission.

Env vars:
  LEETCODE_SESSION     (required) value of the LEETCODE_SESSION cookie from leetcode.com
  LEETCODE_CSRF_TOKEN  (optional) value of the csrftoken cookie
  MAX_PAGES            (optional) stop after this many pages of 20 submissions (default: no limit)
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / ".leetcode-sync.json"
BASE = "https://leetcode.com"

SESSION = os.environ.get("LEETCODE_SESSION", "").strip()
CSRF = os.environ.get("LEETCODE_CSRF_TOKEN", "").strip()
MAX_PAGES = int(os.environ.get("MAX_PAGES", "0") or 0)

EXT = {
    "cpp": "cpp", "java": "java", "python": "py", "python3": "py", "c": "c",
    "csharp": "cs", "javascript": "js", "typescript": "ts", "php": "php",
    "swift": "swift", "kotlin": "kt", "dart": "dart", "golang": "go",
    "ruby": "rb", "scala": "scala", "rust": "rs", "racket": "rkt",
    "erlang": "erl", "elixir": "ex", "mysql": "sql", "mssql": "sql",
    "oraclesql": "sql", "postgresql": "sql", "pythondata": "py", "bash": "sh",
}


def request(path, payload=None):
    headers = {
        "Cookie": f"LEETCODE_SESSION={SESSION}; csrftoken={CSRF}",
        "x-csrftoken": CSRF,
        "Referer": BASE + "/",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36",
    }
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 401:
                sys.exit("LeetCode rejected the request (401). Your LEETCODE_SESSION "
                         "cookie has expired - refresh the repository secret.")
            if e.code == 403:
                # Either an expired cookie or LeetCode's bot protection blocking this
                # runner's IP. The latter is often transient, so back off and retry.
                if attempt == 4:
                    sys.exit(
                        "LeetCode kept returning 403. Either your LEETCODE_SESSION "
                        "cookie is stale (grab a fresh one from your browser and update "
                        "the secret), or LeetCode is temporarily blocking this GitHub "
                        "runner - in which case a later run will go through on its own."
                    )
                time.sleep(20 * 2 ** attempt)
                continue
            if e.code == 429 or e.code >= 500:
                time.sleep(5 * 2 ** attempt)
                continue
            raise
        except urllib.error.URLError:
            time.sleep(5 * 2 ** attempt)
    raise RuntimeError(f"Giving up on {path} after repeated failures")


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_timestamp": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def fetch_new_accepted(since):
    """Return accepted submissions newer than `since`, oldest first."""
    found, offset, last_key, page = [], 0, "", 0
    while True:
        data = request(f"/api/submissions/?offset={offset}&limit=20&lastkey={last_key}")
        if "submissions_dump" not in data:
            sys.exit(f"Unexpected response from LeetCode: {str(data)[:200]}")
        if not data["submissions_dump"] and offset == 0 and since == 0:
            print("No submissions returned - check that LEETCODE_SESSION is valid.")
        done = False
        for s in data["submissions_dump"]:
            if int(s["timestamp"]) <= since:
                done = True
                break
            if s.get("status_display") == "Accepted":
                found.append(s)
        page += 1
        if done or not data.get("has_next") or (MAX_PAGES and page >= MAX_PAGES):
            break
        offset += 20
        last_key = data.get("last_key", "")
        time.sleep(1.5)
    found.sort(key=lambda s: int(s["timestamp"]))
    return found


_question_cache = {}


def question_info(slug):
    if slug not in _question_cache:
        query = """query q($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionFrontendId title difficulty topicTags { name }
          }
        }"""
        data = request("/graphql", {"query": query, "variables": {"titleSlug": slug}})
        _question_cache[slug] = data["data"]["question"]
    return _question_cache[slug]


def git(*args, env=None):
    return subprocess.run(["git", *args], cwd=ROOT, env=env, check=True,
                          capture_output=True, text=True).stdout


def commit_submission(sub, state):
    slug = sub["title_slug"]
    q = question_info(slug)
    folder = ROOT / f"{int(q['questionFrontendId']):04d}-{slug}"
    folder.mkdir(exist_ok=True)

    ext = EXT.get(sub["lang"], "txt")
    (folder / f"{slug}.{ext}").write_text(sub["code"].rstrip() + "\n", encoding="utf-8")

    tags = ", ".join(t["name"] for t in q["topicTags"]) or "-"
    (folder / "README.md").write_text(
        f"# [{q['questionFrontendId']}. {q['title']}]({BASE}/problems/{slug}/)\n\n"
        f"**Difficulty:** {q['difficulty']}  \n"
        f"**Topics:** {tags}\n",
        encoding="utf-8",
    )

    state["last_timestamp"] = int(sub["timestamp"])
    save_state(state)

    git("add", str(folder), str(STATE_FILE))
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        print(f"  unchanged: {q['title']} ({sub['lang']})")
        return False

    when = datetime.fromtimestamp(int(sub["timestamp"]), tz=timezone.utc).isoformat()
    env = {**os.environ, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
    message = (f"{q['questionFrontendId']}. {q['title']} ({q['difficulty']}) - {sub['lang']}\n\n"
               f"Runtime: {sub.get('runtime', '?')}, Memory: {sub.get('memory', '?')}\n"
               f"{BASE}/submissions/detail/{sub['id']}/")
    git("commit", "-m", message, env=env)
    print(f"  committed: {q['title']} ({sub['lang']})")
    return True


def main():
    if not SESSION:
        sys.exit("LEETCODE_SESSION is not set.")
    state = load_state()
    subs = fetch_new_accepted(state["last_timestamp"])
    print(f"Found {len(subs)} new accepted submission(s).")
    commits = sum(commit_submission(s, state) for s in subs)
    print(f"Made {commits} commit(s).")


if __name__ == "__main__":
    main()
