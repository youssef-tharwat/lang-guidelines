# typescript-guidelines: always-load files vs compiled rule card

Date: 2026-10-22. Question: does replacing the "always read three files" skill with a
compiled rule card (design rules), a bundled `oxlintrc.jsonc` (Tier 1–2 lint rules) and
on-demand detail files cut token use without losing compliance?

## Protocol

- **Command:** `evals/run-ab.sh typescript-guidelines <before-skill-copy> <out>`, 3 runs
  per case, `claude-opus-5-5`, judge model `haiku` (CLI default), `--allow-tools Write`
  (no Bash, so neither arm could run Oxlint: the after arm is judged on its card alone),
  `--keep-temp`.
- **Harness:** Claude Code 2.1.308, `claude plugin eval`, macOS, 2026-10-22 15:51 UTC.
- **Repo base:** `30643b44ae1a776768709967057cbd5177e0933c` plus the uncommitted working tree.
- **Before arm:** `typescript-guidelines/` before the restructure (`SKILL.md` told the
  agent to always read `guidelines.txt`, `design.md` and `patterns.md`; its `design.md`
  was the April extraction with flattened code examples). The sorted per-file sha256
  list hashes to 793a10a6aabdbd5d8e36a0bcfde39812324ffc6529659f2f9ab8c8607073bc1e.
- **After arm:**
  - Sorted per-file sha256 list hash:
    891656b5eabf33bed1e3b0d7a6e312dcf32b2a14c16f3011945354df52d6bd5d.
  - The rule card is built from the Google guide rebuilt from the live page.
  - The committed card differs from the tested one only in the wording of its lint
    sentence.
- **Quantities:**
  - *input tokens* sums input, cache creation and cache read tokens over all turns.
  - *output tokens* includes thinking.
  - *Read calls* counts `Read` tool calls.
  - *cost* is the harness's per-run `costUsd`, excluding the judge.

## Result (means per run; 9 runs per arm)

| arm | score | input tokens | output tokens | Read calls | turns | cost USD | skill fired |
| --- | --- | --- | --- | --- | --- | --- | --- |
| no skill | 0.77 | 27,100 | 4,347 | 0.00 | 2.00 | 0.16 | - |
| before | 0.90 | 246,304 | 5,816 | 3.00 | 7.44 | 0.87 | 9/9 |
| after | 0.97 | 55,084 | 3,552 | 0.22 | 4.22 | 0.21 | 9/9 |

Per case (score / input tokens / cost):

| case | no skill | before | after |
| --- | --- | --- | --- |
| cart-class | 1.00 / 27,612 / 0.18 | 0.89 / 323,555 / 0.95 | 1.00 / 61,722 / 0.24 |
| refactor-module | 0.41 / 26,076 / 0.13 | 0.90 / 197,807 / 0.76 | 1.00 / 51,558 / 0.17 |
| user-client | 0.90 / 27,611 / 0.19 | 0.90 / 217,549 / 0.90 | 0.91 / 51,971 / 0.21 |

No run read the eval suite (`no-grader-peeking` passed in every run).

## Reading

- **Tokens and cost:** after uses 78% fewer input tokens than before (55k vs 246k), 39%
  fewer output tokens, 43% fewer turns, and 76% less cost per task.
- **Compliance:** higher (0.97 vs 0.90). The skill matters most on `refactor-module`
  (0.41 without it).
- **Detail files:** the after arm opened a detail file in 2 of 9 runs (0.22 Read calls
  per run).
- **Limits:**
  - n = 3 per case, one model, one judge, three cases.
  - `user-client`'s rubric failed one run in every arm, so it does not separate them.
