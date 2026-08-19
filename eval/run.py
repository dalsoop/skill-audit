#!/usr/bin/env python3
"""skill-audit eval. Default: this skill. --target DIR: checklist on another skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check import check_dir, frontmatter  # noqa: E402

EVAL = json.loads((ROOT / "eval" / "eval.json").read_text(encoding="utf-8"))


def self_check() -> list[str]:
    import re

    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    fm = frontmatter(text)
    desc = re.sub(r"\s+", " ", fm.get("description", ""))
    failed = check_dir(ROOT)
    if fm.get("name") != EVAL["skill"]:
        failed.append(f"name {fm.get('name')!r}")
    for t in EVAL["triggers_required"]:
        if t not in desc:
            failed.append(f"description missing {t!r}")
    for n in EVAL["needles"]:
        if n not in text:
            failed.append(f"body missing {n!r}")
    vf = ROOT / "VERSION"
    if not vf.is_file():
        failed.append("missing VERSION")
    return failed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, help="skill directory to checklist")
    args = ap.parse_args()
    if args.target:
        root = args.target.expanduser().resolve()
        failed = check_dir(root)
        print(json.dumps({"target": str(root), "ok": not failed, "failed": failed}, indent=2, ensure_ascii=False))
        return 1 if failed else 0
    failed = self_check()
    print(json.dumps({"ok": not failed, "failed": failed}, indent=2, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
