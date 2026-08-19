#!/usr/bin/env python3
"""Checklist runner for a skill directory. Used by skill-audit eval."""

from __future__ import annotations

import re
from pathlib import Path

HANGUL = re.compile(r"[\uac00-\ud7a3]")
EN_TRIGGERS = ("expert consult", "second opinion", "consultant gate")
META = {
    "skill-audit",
    "skill-multi-model-overconfidence-guard",
    "skill-glm-delegation-with-brief",
}


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        raise ValueError("SKILL.md: missing YAML frontmatter")
    out: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in m.group(1).splitlines():
        if re.match(r"^[a-zA-Z0-9_-]+:", line) and not line.startswith(" "):
            if key is not None:
                out[key] = "\n".join(buf).strip().strip("\"'")
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest in (">", ">|"):
                buf = []
            else:
                buf = [rest]
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        out[key] = "\n".join(buf).strip().strip("\"'")
    meta = re.search(r"^metadata:\n((?:  .*\n)+)", m.group(1) + "\n", re.M)
    if meta:
        vm = re.search(r"version:\s*[\"']?([0-9]+\.[0-9]+\.[0-9]+)", meta.group(1))
        if vm:
            out["metadata.version"] = vm.group(1)
        lm = re.search(r"locale:\s*[\"']?(\w+)", meta.group(1))
        if lm:
            out["metadata.locale"] = lm.group(1)
    return out


def locale_of(name: str, fm: dict[str, str]) -> str:
    if name in META:
        return "meta"
    loc = fm.get("metadata.locale", "")
    if loc in ("en", "ko"):
        return loc
    if name.endswith("-ko"):
        return "ko"
    return "en"


def check_dir(root: Path) -> list[str]:
    failed: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return [f"missing {skill}"]
    text = skill.read_text(encoding="utf-8")
    try:
        fm = frontmatter(text)
    except ValueError as e:
        return [str(e)]
    name = fm.get("name", "")
    desc = re.sub(r"\s+", " ", fm.get("description", ""))
    loc = locale_of(name, fm)
    if name != root.name:
        failed.append(f"name {name!r} != folder {root.name!r}")
    vf = root / "VERSION"
    ver = fm.get("metadata.version") or fm.get("version", "")
    if vf.is_file():
        disk = vf.read_text(encoding="utf-8").strip()
        if disk != ver:
            failed.append(f"VERSION {disk!r} != frontmatter {ver!r}")
    for nested in ("ko", "en"):
        p = root / nested
        if p.is_dir() and (p / "SKILL.md").is_file():
            failed.append(f"nested {nested}/ folder")
    readme = root / "README.md"
    rm = ""
    if readme.is_file():
        rm = readme.read_text(encoding="utf-8")
        blob = text + "\n" + rm
        if re.search(r"skills add \S+#ko", rm):
            failed.append("README uses #ko; want @ko")
        if loc == "en" and "how-the-gate-works-ko.png" in rm:
            failed.append("en README has ko diagram")
        if loc == "ko" and "how-the-gate-works-en.png" in rm:
            failed.append("ko README has en diagram")
        if loc == "ko" and "@ko" not in rm and "npx skills add" in rm:
            failed.append("ko README missing @ko install")
        if loc == "en" and re.search(r"\bplan\b", rm, re.I) and "plan" not in text.lower():
            failed.append("README plan missing from SKILL (same object)")
        if loc == "ko" and "계획" in rm and "계획" not in text:
            failed.append("README 계획 missing from SKILL (same object)")
    else:
        blob = text
    if "resolve-consult.py" in text:
        if "--name grok" not in text:
            failed.append("resolve-consult.py without --name grok fallback")
        if "fallback_slug" not in text:
            failed.append("consult spawn missing fallback_slug")
        if "--record" not in text:
            failed.append("consult spawn missing --record (observability)")
        if readme.is_file() and "npx skills add" in rm:
            cave = rm.lower()
            if "files" not in cave and "파일" not in rm:
                failed.append("public install README missing files vs host spawn")
    if loc != "meta" and "opus-fable-orchestrator" in blob:
        failed.append("legacy opus-fable-orchestrator in SKILL.md/README")
    if loc == "en":
        if HANGUL.search(desc):
            failed.append("en description has Hangul triggers")
        if name.endswith("-ko"):
            failed.append("en locale but name ends -ko")
    elif loc == "ko":
        if not name.endswith("-ko"):
            failed.append("ko locale but name missing -ko suffix")
        extra = [t for t in EN_TRIGGERS if t in desc]
        if extra:
            failed.append(f"ko description has English triggers {extra}")
        if not HANGUL.search(desc):
            failed.append("ko description has no Hangul")
    return failed
