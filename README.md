# LeetCode Solutions

My accepted LeetCode solutions. Each problem has its own folder with the solution
and a short README linking back to the problem. Everything here is synced
automatically by a GitHub Action, and every commit is dated to the moment I
actually submitted it.

The table below is generated from the folders by `scripts/make_index.py`.

<!-- BEGIN SOLUTIONS -->
**24 problems solved** — 16 easy, 8 medium, 0 hard.

| # | Problem | Difficulty | Topics | Language | Last solved |
| ---: | --- | --- | --- | --- | --- |
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | Array, Hash Table | [Java, Python](0001-two-sum/) | 2026-10-30 |
| 3 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Hash Table, String, Sliding Window | [Java](0003-longest-substring-without-repeating-characters/) | 2026-10-30 |
| 11 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Array, Two Pointers, Greedy | [Java](0011-container-with-most-water/) | 2026-10-30 |
| 26 | [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | Easy | Array, Two Pointers | [Java](0026-remove-duplicates-from-sorted-array/) | 2026-10-30 |
| 73 | [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | Medium | Array, Hash Table, Matrix | [Java](0073-set-matrix-zeroes/) | 2026-10-30 |
| 88 | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | Easy | Array, Two Pointers, Sorting | [Java](0088-merge-sorted-array/) | 2026-10-30 |
| 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Array, Dynamic Programming | [Java](0121-best-time-to-buy-and-sell-stock/) | 2026-10-30 |
| 125 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy | Two Pointers, String | [Java](0125-valid-palindrome/) | 2026-10-30 |
| 151 | [Reverse Words in a String](https://leetcode.com/problems/reverse-words-in-a-string/) | Medium | Two Pointers, String | [Java](0151-reverse-words-in-a-string/) | 2026-10-30 |
| 169 | [Majority Element](https://leetcode.com/problems/majority-element/) | Easy | Array, Hash Table, Divide and Conquer, Sorting, Counting, Boyer–Moore Majority Vote Algorithm | [Java](0169-majority-element/) | 2026-10-30 |
| 189 | [Rotate Array](https://leetcode.com/problems/rotate-array/) | Medium | Array, Math, Two Pointers | [Java](0189-rotate-array/) | 2026-10-30 |
| 209 | [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | Medium | Array, Binary Search, Sliding Window, Prefix Sum | [Java](0209-minimum-size-subarray-sum/) | 2026-10-30 |
| 217 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Easy | Array, Hash Table, Sorting | [Java, Python](0217-contains-duplicate/) | 2026-10-30 |
| 226 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Easy | Tree, Depth-First Search, Breadth-First Search, Binary Tree | [Python](0226-invert-binary-tree/) | 2026-10-30 |
| 238 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Array, Prefix Sum | [Java](0238-product-of-array-except-self/) | 2026-10-30 |
| 242 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Easy | Hash Table, String, Sorting | [Java, Python](0242-valid-anagram/) | 2026-10-30 |
| 345 | [Reverse Vowels of a String](https://leetcode.com/problems/reverse-vowels-of-a-string/) | Easy | Two Pointers, String | [Java](0345-reverse-vowels-of-a-string/) | 2026-10-30 |
| 392 | [Is Subsequence](https://leetcode.com/problems/is-subsequence/) | Easy | Two Pointers, String, Dynamic Programming | [Java](0392-is-subsequence/) | 2026-10-30 |
| 560 | [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Array, Hash Table, Prefix Sum | [Java](0560-subarray-sum-equals-k/) | 2026-10-30 |
| 605 | [Can Place Flowers](https://leetcode.com/problems/can-place-flowers/) | Easy | Array, Greedy | [Java](0605-can-place-flowers/) | 2026-10-30 |
| 1071 | [Greatest Common Divisor of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/) | Easy | Math, String, Euclidean Algorithm, Greatest Common Divisor | [Java](1071-greatest-common-divisor-of-strings/) | 2026-10-30 |
| 1431 | [Kids With the Greatest Number of Candies](https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/) | Easy | Array | [Java](1431-kids-with-the-greatest-number-of-candies/) | 2026-10-30 |
| 1768 | [Merge Strings Alternately](https://leetcode.com/problems/merge-strings-alternately/) | Easy | Two Pointers, String | [Java](1768-merge-strings-alternately/) | 2026-10-30 |
| 1929 | [Concatenation of Array](https://leetcode.com/problems/concatenation-of-array/) | Easy | Array, Simulation | [Java](1929-concatenation-of-array/) | 2026-10-30 |

<!-- END SOLUTIONS -->

## How the sync works

`.github/workflows/sync-leetcode.yml` runs every 30 minutes, calls
`scripts/sync.py` to pull any new accepted submissions, commits each one
separately, then regenerates the table above.

### Setup

1. Log in to leetcode.com → DevTools (F12) → **Application** → **Cookies** →
   `https://leetcode.com`. Copy the values of `LEETCODE_SESSION` and `csrftoken`.
2. In this repo: **Settings → Secrets and variables → Actions → New repository secret**:
   - `LEETCODE_SESSION` = the `LEETCODE_SESSION` cookie value
   - `LEETCODE_CSRF_TOKEN` = the `csrftoken` cookie value
3. **Actions** tab → **Sync LeetCode** → **Run workflow** for the first sync.

### Notes

- The session cookie expires every few weeks. When a run fails with
  "cookie is probably expired", copy fresh cookie values into the secrets.
- `LEETCODE_SESSION` is as sensitive as a password: it lives only in GitHub
  Secrets, never in this repo.
- `.leetcode-sync.json` records the newest synced submission so nothing is
  committed twice.
- Run locally: `LEETCODE_SESSION=... python scripts/sync.py`, then
  `python scripts/make_index.py`. Set `MAX_PAGES=1` to test quickly.
