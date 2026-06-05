# Mission

## Purpose

Build a medical condition briefing system that generates accurate, structured summaries for health system professionals by synthesizing information from live medical data sources.

## Problem Statement

Health strategy teams and clinical practitioners lack a fast, reliable way to get a consolidated view of a medical condition — covering what is currently standard of care, what is in the pipeline, and who the key players are. Existing tools require navigating multiple databases manually, and output is fragmented and unstructured.

## Primary Users

- **Health system strategy teams** — need condition overviews to inform investment, partnership, and care delivery decisions
- **Clinicians and care teams** — need concise, current summaries of treatment options and emerging therapies when evaluating patient care paths

## Core Output

Given a medical condition as input, the system produces a structured brief containing:

1. **Standard of Care** — current first-line and guideline-endorsed treatments
2. **Emerging Treatments** — therapies in clinical trials or late-stage development
3. **Key Organizations** — pharma companies, research institutions, and hospitals driving progress

## Delivery

The system is accessible two ways:

- **Web UI** — a minimal React interface where users type a condition and receive a formatted brief; intended for direct use by strategy teams and clinicians
- **REST API** — a `POST /brief` endpoint for programmatic access or integration into larger health system platforms

## Success Criteria

- **Accuracy is the primary measure** — briefings must reflect current, evidence-based information from authoritative sources
- Speed is secondary; a brief that is fast but wrong is worse than one that is slightly slower but correct
- Sources must be traceable (PubMed IDs, ClinicalTrials.gov NCT numbers, institution names)
- The UI must be usable without technical knowledge — a clinician should be able to get a brief without reading any documentation
