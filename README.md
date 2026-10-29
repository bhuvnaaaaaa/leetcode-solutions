# LeetCode Solutions

My accepted LeetCode solutions, synced automatically by a GitHub Action
(`.github/workflows/sync-leetcode.yml`). Each accepted submission becomes its own
commit, dated at the time I submitted it.

Layout: `0001-two-sum/two-sum.py` + `0001-two-sum/README.md` (problem link, difficulty, topics).

## Setup

1. Push this folder to a new GitHub repo.
2. Log in to leetcode.com in your browser → DevTools (F12) → **Application** → **Cookies** →
   `https://leetcode.com`. Copy the values of `LEETCODE_SESSION` and `csrftoken`.
3. In the GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**:
   - `LEETCODE_SESSION` = the `LEETCODE_SESSION` cookie value
   - `LEETCODE_CSRF_TOKEN` = the `csrftoken` cookie value
4. **Actions** tab → **Sync LeetCode** → **Run workflow** to do the first sync.
   The first run backfills your whole history; after that it runs every 30 minutes.

## Notes

- The session cookie expires every few weeks (or when you log out). When a run fails with
  "cookie is probably expired", copy fresh cookie values into the secrets.
- Treat `LEETCODE_SESSION` like a password: it only lives in GitHub Secrets, never in the repo.
- `.leetcode-sync.json` records the newest synced submission so nothing is committed twice.
- Run locally: `LEETCODE_SESSION=... python scripts/sync.py` (set `MAX_PAGES=1` to test quickly).
