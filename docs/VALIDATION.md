# Validation

The demonstration workflow generates four validation gates:

- initial energy matches the configured reference value
- divergence remains below a strict numerical bound
- kinetic energy remains positive
- the replay changes state under lid-driven forcing

Run locally:

```bash
python -m polymathica_hackathon.cli --output demo/output
python -m unittest discover -s tests
```

Generated evidence:

- `demo/output/experiment_config.json`
- `demo/output/replay_samples.json`
- `demo/output/validation_report.json`
- `demo/output/validation_trace.svg`
- `demo/output/report.html`
- `demo/output/provenance.json`
- `demo/output/archive_manifest.json`

![Validation trace](assets/validation_trace.svg)
