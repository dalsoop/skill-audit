# skill-audit

Score and slim existing agent `SKILL.md` files. Delete pitch. Keep procedures. One locale per git branch (not a nested `ko/` folder).

```bash
npx skills add dalsoop/skill-audit -g -y
python3 eval/run.py
python3 eval/run.py --target /path/to/skill
```

`npx` copies **files**. This skill does not spawn a child. A fail from `--target` is not a passing score.

Family (install separately):

```bash
npx skills add dalsoop/orchestrator-consultant-gate -g -y
npx skills add dalsoop/skill-multi-model-overconfidence-guard -g -y
npx skills add dalsoop/skill-glm-delegation-with-brief -g -y
```

[`SKILL.md`](SKILL.md) · [`eval/`](eval/) · MIT

[![skills.sh](https://skills.sh/b/dalsoop/skill-audit)](https://skills.sh/dalsoop/skill-audit)
