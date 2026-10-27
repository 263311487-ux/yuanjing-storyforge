# Security Policy

## Reporting

If you find a security issue in yuanjing-storyforge:

1. Do **not** open a public issue.
2. Email: 263311487@qq.com — description, reproduction steps, severity.
3. Response within 72 hours.

## Scope

- Manifest parsing (path traversal, schema injection)
- Provider adapter credential handling (keys must not appear in logs or manifests)
- The approval record system (hash binding, file integrity)

## Notes

- Provider credentials (API keys, tokens) must never be committed to manifests or run state. The adapter layer is responsible for sourcing them from environment variables.
- The approval hash system (`scripts/approve_publish.py`) binds file hashes at approval time. Changing a bound file after approval invalidates the record — this is by design, not a bug.
