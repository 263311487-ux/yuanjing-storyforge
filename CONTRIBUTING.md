# Contributing to Yuanjing Storyforge (元境·漫界工坊)

## What we welcome

- **Manifest validator improvements**: edge cases the current schema or continuity checker misses
- **New script utilities**: offline tools that work without paid providers
- **Provider adapters**: documented adapters for video generation services (must require explicit `execute=True` opt-in — no silent API calls)
- **Test cases**: new manifest fixtures that expose validation gaps
- **Documentation**: clearer workflow guides, translation fixes, platform-specific setup notes

## Development setup

```bash
git clone https://github.com/263311487-ux/yuanjing-storyforge.git
cd yuanjing-storyforge
pip install .
python scripts/quickstart.py
python -m unittest discover -s tests -p 'test_*.py'
```

No paid API key needed — the offline workflow uses the mock provider.

## Pull request checklist

- [ ] `python -m unittest discover -s tests -p 'test_*.py'` passes
- [ ] `python scripts/quickstart.py` completes with `READY_FOR_PROVIDER_REVIEW`
- [ ] New provider adapters use `execute=False` by default and require explicit opt-in
- [ ] No real video generation calls in CI (CI must stay free to run)
- [ ] New scripts have a `--help` flag and exit cleanly without arguments

## Provider adapter guidelines

Provider adapters live in `ai_comic_drama/providers.py`. An adapter must:

1. Accept a manifest and a shot ID
2. Construct the provider request without submitting it by default
3. Require `execute=True` to actually submit
4. Return a structured result with a status field (not a raw provider response)
5. Log budget consumed, not just success/failure

## Manifest schema changes

Changes to the manifest schema (fields, validation rules, required vs optional) need:
- A migration note in `references/manifest-schema.md`
- Backward compatibility or a clear breaking-change notice in the commit
- At least one new test fixture exercising the new/changed field
