#!/usr/bin/env python3
"""Local, read-only checks for Markdown knowledge exports."""

import argparse
import datetime as dt
import json
import re
from pathlib import Path

import yaml

MESSAGES = {
    "frontmatter_missing": {"fr": "Métadonnées absentes.", "en": "Missing metadata.", "es": "Faltan metadatos."},
    "frontmatter_invalid": {"fr": "Métadonnées illisibles.", "en": "Invalid metadata.", "es": "Metadatos no válidos."},
    "source_missing": {"fr": "Source absente.", "en": "Missing source.", "es": "Falta la fuente."},
    "stale": {"fr": "Connaissance périmée.", "en": "Stale knowledge.", "es": "Conocimiento obsoleto."},
    "date_invalid": {"fr": "Date de péremption invalide.", "en": "Invalid expiry date.", "es": "Fecha de caducidad no válida."},
    "secret_pattern": {"fr": "Secret potentiel détecté.", "en": "Possible secret detected.", "es": "Posible secreto detectado."},
    "fact_conflict": {"fr": "Valeurs incompatibles pour le même fait.", "en": "Conflicting values for the same fact.", "es": "Valores incompatibles para el mismo hecho."},
}
SECRET_PATTERNS = [
    re.compile(r"(?i)\b(?:sk|rk)-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*[\"']?[A-Za-z0-9_./+-]{16,}"),
]


def split_frontmatter(content):
    if not content.startswith("---\n"):
        return None, content
    end = content.find("\n---\n", 4)
    if end < 0:
        return None, content
    try:
        metadata = yaml.safe_load(content[4:end]) or {}
    except yaml.YAMLError:
        return False, content[end + 5 :]
    if not isinstance(metadata, dict):
        return False, content[end + 5 :]
    return metadata, content[end + 5 :]


def parse_date(value):
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            pass
    return None


def scan(root, today=None, lang="fr"):
    today = today or dt.date.today()
    if lang not in ("fr", "en", "es"):
        raise ValueError("E_LANGUAGE")
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("E_DIRECTORY")
    issues = []
    facts = {}
    files = sorted(root.rglob("*.md"))
    for path in files:
        relative = str(path.relative_to(root))
        if path.is_symlink():
            continue
        content = path.read_text(encoding="utf-8")
        metadata, body = split_frontmatter(content)

        def issue(code, related=None):
            item = {"file": relative, "code": code, "message": MESSAGES[code][lang]}
            if related:
                item["related_file"] = related
            issues.append(item)

        if metadata is None:
            issue("frontmatter_missing")
            metadata = {}
        elif metadata is False:
            issue("frontmatter_invalid")
            metadata = {}
        if not metadata.get("sources") and not metadata.get("source"):
            issue("source_missing")
        if "stale_after" in metadata:
            expiry = parse_date(metadata["stale_after"])
            if not expiry:
                issue("date_invalid")
            elif expiry < today:
                issue("stale")
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            issue("secret_pattern")
        key = metadata.get("fact_key")
        value = metadata.get("fact_value")
        if isinstance(key, str) and key.strip() and isinstance(value, (str, int, float, bool)):
            normalized_key = key.strip().casefold()
            normalized_value = str(value).strip()
            if normalized_key in facts and facts[normalized_key][0] != normalized_value:
                issue("fact_conflict", facts[normalized_key][1])
            else:
                facts[normalized_key] = (normalized_value, relative)
    return {
        "status": "clean" if not issues else "attention",
        "language": lang,
        "files_checked": len(files),
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Examiner un export Markdown / Check a Markdown export / Revisar una exportación Markdown"
    )
    parser.add_argument("directory")
    parser.add_argument("--lang", choices=("fr", "en", "es"), default="fr")
    parser.add_argument("--today", help="YYYY-MM-DD")
    args = parser.parse_args()
    try:
        today = dt.date.fromisoformat(args.today) if args.today else None
        report = scan(args.directory, today=today, lang=args.lang)
    except (ValueError, OSError, UnicodeError):
        parser.exit(1, "E_INPUT\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "clean" else 2


if __name__ == "__main__":
    raise SystemExit(main())
