# python-guidelines: always-load files vs compiled rule card

Date: 2026-10-22. Question: does replacing the "always read three files" skill with a
compiled rule card (design rules), a bundled `ruff.toml` (Tier 1–2 lint rules) and
on-demand detail files cut token use without losing compliance?

## Protocol

- **Command:** `evals/run-ab.sh python-guidelines <before-skill-copy> <out>`, 3 runs per
  case, `claude-opus-5-5`, judge model `haiku` (CLI default), `--allow-tools Write` (no
  Bash, so neither arm could run Ruff: the after arm is judged on its card alone),
  `--keep-temp`.
- **Harness:** Claude Code 2.1.308, `claude plugin eval`, macOS.
- **Repo base:** `30643b44ae1a776768709967057cbd5177e0933c` plus the uncommitted working tree.
- **Before arm:** `python-guidelines/` before the restructure (`SKILL.md` told the agent
  to always read `guidelines.txt`, `design.md` and `patterns.md`); the sorted per-file
  sha256 list hashes to f957da697500028f3814e3b016af27ececd3435999a6d84b70d9ab8c80afb4be.
- **Runs:**
  - `rate-limiter` comes from the full run at 15:51 UTC, after arm
    3731a6b452c967766699f271e189b443423e5a68af56dd3026b792a2b9a5fd8a.
  - `config-loader` and `refactor-module` come from a re-run at about 16:00 UTC, after
    arm 9efc8794b530f1d693a6a0de4a39757eecbdf57fa986397a5e3dab737d1edcf8.
  - The two after arms differ only in the wording of the card's lint sentence.
- **Why the re-run:** two graders in the first run were wrong and failed arms
  regardless of skill.
  - `with-open` rejected `Path.read_text()`, which every before-arm run used and which
    leaves nothing open.
  - `refactor-module`'s rubric demanded hiding a public module-level `CACHE` the prompt
    asked to keep. It failed all nine runs in every arm.
  - Both graders were corrected (see `cases/`) and the two cases re-run in every arm.
    The first run's numbers for them are retired.
- **Quantities:**
  - *input tokens* sums input, cache creation and cache read tokens over all turns.
  - *output tokens* includes thinking.
  - *Read calls* counts `Read` tool calls.
  - *cost* is the harness's per-run `costUsd`, excluding the judge.

## Result (means per run; 9 runs per arm)

| arm | score | input tokens | output tokens | Read calls | turns | cost USD | skill fired |
| --- | --- | --- | --- | --- | --- | --- | --- |
| no skill | 0.82 | 27,843 | 3,279 | 0.00 | 2.11 | 0.13 | - |
| before | 0.93 | 208,003 | 5,166 | 2.11 | 7.55 | 0.58 | 9/9 |
| after | 1.00 | 58,494 | 3,616 | 0.00 | 4.67 | 0.20 | 9/9 |

Per case (score / input tokens / cost):

| case | no skill | before | after |
| --- | --- | --- | --- |
| config-loader | 0.80 / 25,523 / 0.12 | 1.00 / 285,391 / 0.72 | 1.00 / 55,485 / 0.18 |
| refactor-module | 0.67 / 25,286 / 0.10 | 0.78 / 82,314 / 0.30 | 1.00 / 61,752 / 0.17 |
| rate-limiter | 1.00 / 32,681 / 0.18 | 1.00 / 256,271 / 0.71 | 1.00 / 58,254 / 0.24 |

No run read the eval suite (`no-grader-peeking` passed in every run).

## Reading

- **Tokens and cost:** after uses 72% fewer input tokens than before (58k vs 208k), 30%
  fewer output tokens, 38% fewer turns, and 66% less cost per task.
- **Compliance:** higher (1.00 vs 0.93), driven by `refactor-module`, where the old skill
  often skipped its own required reading (0.67 Read calls per run there).
- **Detail files:** the after arm never opened a detail file. It also met the
  lint-backed checks (mutable defaults, broad `except`, f-string logging, `assert`) from
  the card alone, without running Ruff.
- **Limits:** n = 3 per case, one model, one judge, three cases. `rate-limiter` does not
  separate the arms.
