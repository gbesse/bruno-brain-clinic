# Bruno Brain Clinic

[Français](README.md) · [Español](README.es.md)

A **local, read-only** checker for agent memory Markdown exports, including [Bruno Brain](https://get-bruno.com/fr/tech). It flags pages without a source, expired knowledge, selected secret patterns, and conflicting values that explicitly share a fact_key. Reports contain neither fact values nor detected secrets.

The skills/brain-clinic directory contains a reusable agent skill for running the local check.

## Try it

    python3 -m pip install -r requirements.txt
    python3 brain_clinic.py EXPORT_PATH --lang en
    python3 -m unittest discover -s tests -v

When present, metadata is YAML between two --- lines at the top of each Markdown file. This version understands sources or source, stale_after as YYYY-MM-DD, and optional fact_key and fact_value for comparing facts. A link in the body can also serve as a source. The program reads all .md files in the directory and emits JSON. Exit codes: 0 no findings, 2 review needed, 1 invalid input. Messages are available in French, English, and Spanish.

Bruno advertises export of its brain in Markdown or OKF. This repository works on exported Markdown files; it does not connect to Bruno or validate the full OKF specification. It detects only contradictions explicitly identified by fact_key, not semantic disagreements. Review findings before making corrections.

MIT licensed.
