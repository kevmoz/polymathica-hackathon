# Verification Dossier

This page is the independent verification path for the public demonstration package.

The repository is intentionally scoped as a compact, reproducible evidence package for the broader POLYMATHICA ecosystem. The verification command checks the committed evidence bundle rather than relying on a narrative summary.

## One-Command Verification

Generate the evidence bundle:

```bash
python -m polymathica_hackathon.suite --output demo
```

Verify the generated bundle:

```bash
python -m polymathica_hackathon.verify --root demo --report demo/verification_report.json
```

Run the full tests:

```bash
python -m unittest discover -s tests
```

## What The Verifier Checks

- `demo/evidence_suite_manifest.json` has the expected schema and `passed` status.
- `demo/evidence_suite_summary.json` has the expected schema and `passed` status.
- all manifest-listed artifact SHA-256 hashes match the files on disk.
- workflow, Taylor-Green, projection and Poiseuille components are present.
- every component reports `passed`.
- validation artifacts for all components report `passed`.
- workflow provenance artifact hashes verify independently.

## Verification Report

The verifier writes:

- `demo/verification_report.json`

The report records:

- verification status
- number of artifacts checked
- number of components checked
- component statuses
- artifact SHA-256 hashes

## Scope

This verifier does not certify the complete private POLYMATHICA platform. It verifies that the public repository's committed demonstration evidence is internally consistent, reproducible and hash-linked.
