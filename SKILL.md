---
name: skill-audit
version: 1.4.1
kind: skill
metadata:
  version: "1.4.1"
description: >-
  Score and slim existing agent SKILL.md files. Delete pitch, origin stories,
  comparison tables, and paper citations. Keep only procedures. Enforce one
  locale per git branch (not a nested ko/ folder). Use when the user asks to
  score a skill, improve a skill, cut skill bloat, rewrite SKILL.md, audit
  skill quality, skill checklist, 스킬 채점, 스킬 개선, 스킬 감량, 다국어 스킬,
  스킬 체크리스트, 스킬 만들기, new skill.
---

# Skill Audit

Do not write a new essay. Do not edit `~/.cursor/skills-cursor/` or `~/.codex/skills/.system/`.
Ignore `~/.codex/skills/.migrated-to-consolidated/` except to stub them.

New skills: draft with `create-skill` / `skill-creator` (do not edit those built-ins), then this audit **and** `--target` before done. Locale rules live here.

## Method

1. SSOT: folder name == `name`. Built-in or migrated → stub only.
2. `python3 eval/run.py --target <skill-dir>`. Any fail → not a passing score.
3. Score **Axes**. Table + total /100.
4. Improve: delete fat, rewrite procedures, re-run. Below 75 → cut once more.
5. If the skill has `eval/run.py`, run it. Public GitHub skills need eval.
6. Family / 전체: every SSOT row; stub copies; no dangling “see X”.
7. Spawn skills: two scores — **files** (npx/eval) vs **live spawn**. Public npx is files, not E2E.

Body ≤80 lines unless a command table needs more. Cap 500.

```bash
python3 eval/run.py
python3 eval/run.py --target /path/to/skill
```

제품: **one locale per git branch** (`main` 영어, `ko` + `name-ko`). 메타: **bilingual file**. `ko/` nested 폴더 금지.

## Checklist (fail closed)

**Locale** — Product: one locale per branch, not nested `ko/` or `en/`. `main` = English `name`. `ko` = `name-ko`. `metadata.locale` matches the branch. Description triggers that locale only. README: `npx skills add <owner>/<repo>`; Korean `@ko` not `#ko`. Diagrams: that locale only.

**Object**

- `name` == folder. `VERSION` == frontmatter version when the file exists.
- Description: third person, WHAT + WHEN. No README voice in SKILL.md.
- Body: steps this turn (commands, templates, if/then, fallback). No pitch, origin, vs-table, papers, FAQ, ROI.
- **Same object:** SKILL, README, and diagram name one artifact (plan, not a code review, not a second executor). WHEN is the work order / audit-then-change, not merge-only. Caption ≠ flow → fail.
- **Spawn fallback:** default child blocked (data policy, 402) → `fallback_slug` / `--name grok` once, or skip+retry at next gate. Do not stall.
- **Host spawn:** resolve JSON includes `spawn` for this host. Do not call another host’s model list.
- **Observability:** after a consult, record host+slug+read_only (digest or `--record`).
- **Public:** host-private CLIs need an in-repo fallback. README with `npx skills add` must say files vs host spawn.
- **Examples:** do not fill diagrams with stock critiques (`no tests`, `missing rollback`). Empty or one real artifact.
- Do not hardcode the parent model. Session stays. Child slugs from registry + host.
- One trigger → one family row.

**Done when** Checklist passes, score ≥75 with fat=20 (or fat=16 and procedure≥20), eval passes if present.

## Axes (100)

| Axis | Pts | Full |
|---|---|---|
| Procedure | 25 | steps the agent can run now |
| Fat | 20 | no pitch/origin/vs-table/papers/FAQ |
| Executable | 20 | commands, templates, if/then |
| Description | 10 | third person, WHAT + WHEN |
| Verifiable | 15 | pass/fail, command, or explicit skip |
| Disclosure | 10 | lean SKILL.md; details linked |

**Auto-cut:** pitch, origin, vs-table, citation, ROI, domain menu with no steps.

Fail if it teaches what the model already knows, or the rewrite adds non-procedures. Do not add the files score and the live-spawn score.

## Family

| Job | Skill |
|---|---|
| Slim/score SKILL.md | `skill-audit` |
| Consultant gate (en) | `orchestrator-consultant-gate` |
| Consultant gate (ko) | `orchestrator-consultant-gate-ko` |
| Budget + Grok + prompt | `skill-multi-model-overconfidence-guard` |
| GLM mechanical | `skill-glm-delegation-with-brief` |

Delete first. This skill: `python3 eval/run.py`. Others: `--target <dir>`.
