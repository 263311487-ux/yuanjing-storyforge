# Yuanjing Storyforge · 元境·漫界工坊

**Yuanjing Storyforge** (元境·漫界工坊), formerly `ai-comic-drama`, is the unique name of this manifest-first comic-drama production skill. Search compatibility keywords: AI comic drama, AI short drama, 漫剧 skill.

Source release **1.9.3**, published 2026-10-09. The repository exposes a zero-runtime-dependency Python compatibility package named `yuanjing-storyforge`; its import module remains `ai_comic_drama` for compatibility.

[![CI](https://github.com/263311487-ux/yuanjing-storyforge/actions/workflows/ci.yml/badge.svg)](https://github.com/263311487-ux/yuanjing-storyforge/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/263311487-ux/yuanjing-storyforge)](https://github.com/263311487-ux/yuanjing-storyforge/releases)

Manifest-first Agent Skill for planning and validating AI comic-drama production. It provides provider-neutral contracts, offline resumable runs, cost gates, subtitle and assembly planning, optional encoding, technical QA, and auditable human review gates.

**Keywords:** AI comic drama, AI short drama, storyboard manifest, Seedance workflow, video generation pipeline, Codex Agent Skill, technical QA, human content review.

It is safe to try locally: examples and CI do not call paid providers. Video generation remains an explicit provider opt-in.

## Install as an agent skill

Use the canonical repository `263311487-ux/yuanjing-storyforge`; do not choose a similarly named AI comic-drama skill. Copy this repository into your agent skills directory as `yuanjing-storyforge`, or use your agent's skill installer with `https://github.com/263311487-ux/yuanjing-storyforge`. The invocation name is `$yuanjing-storyforge`, and the entry point is [`SKILL.md`](SKILL.md). Python 3.11+ and the standard library are enough for the offline workflow.

For Python integrations, install the compatibility package locally from a clone (not published to PyPI):

```sh
python3 -m pip install .
```

This installs `ai_comic_drama`; it does not install a provider CLI, ffmpeg, or paid-service credentials.

The shortest offline example is documented in [`examples/offline-output/README.md`](examples/offline-output/README.md). Citation metadata is available in [`CITATION.cff`](CITATION.cff).

## First success in one minute

From the repository root, use Python 3.11 or newer:

```sh
python3 --version
python3 scripts/quickstart.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Open `work/quickstart/previz.html`, then inspect `quickstart.json` for the artifact index. A successful planning run reports `READY_FOR_PROVIDER_REVIEW`; the mock succeeds without creating any video. `assembly.json` is correctly `blocked` until real clips exist, and `qa_result.json` stays `PENDING_HUMAN_REVIEW`. These are expected safeguards, not a failed quickstart.

[See the committed synthetic example outputs](examples/offline-output/README.md): a two-shot, 11-second text storyboard, SRT, blocked assembly plan, and pending review report, captured from a real offline run. No generated character art or paid-provider result is represented.

| Local task | Requirements | Tested scope |
|---|---|---|
| Manifest, quickstart, mock and planning | Python 3.11+ standard library | Ubuntu CI; macOS local |
| Optional disposable MP4 and technical QA | `ffmpeg` and `ffprobe` on PATH, with libx264 and AAC encoders | macOS local; not required for first success |
| Windows use | Python 3.11+ (`py -3.11` may replace `python3`); optional encoder binaries on PATH | Not a current CI target; validate locally |
| Actual video generation | Separately installed provider, approved budget and explicit execution | Not exercised by offline examples |

## What it does

- Offline shot-manifest checks.
- Text storyboard HTML (not a visual animatic).
- Cost estimates using user-supplied per-second rates.
- Content-review records with explicit `PASS`, `PENDING_HUMAN_REVIEW`, and `FAIL` states.
- Separate publish approval records bound to the reviewed report hash.

It does not claim automated story judgment, platform compliance approval, or unattended paid generation.

## Offline runner

### Review a manifest at a glance

```sh
python3 scripts/manifest_report.py work/my-episode.json
```

Use `--json` for CI or issue reports. It summarizes duration, dialogue coverage, assets, provider, and budget without contacting a provider.

### Check shot continuity

```sh
python3 scripts/continuity_check.py work/my-episode.json --json
```

This catches broken `continuity_from` links and unknown character or scene IDs before generation.

### Diagnose the local environment

```sh
python3 scripts/doctor.py
```

The doctor reports Python, optional `ffmpeg`/`ffprobe`, the optional Seedance CLI, and offline manifest readiness. It never submits a paid request.

### Start a new manifest

Create an editable episode contract without copying JSON by hand:

```sh
python3 scripts/init_manifest.py --out work/my-episode.json --title "My Episode"
```

Fill the marked shot and release fields, then run `scripts/validate_manifest.py` before quickstart.
For a production handoff, use `python3 scripts/validate_manifest.py work/my-episode.json --strict` to require release metadata and complete shot fields.

### One-command quickstart

Run the complete provider-neutral first-success workflow:

```sh
python3 scripts/quickstart.py
```

It validates the manifest, generates a text previz, creates a pending human-review report, writes subtitles and an assembly plan, runs the offline resumable mock, and writes `work/quickstart/quickstart.json`. No paid API is called.

The mock provider exercises resumable state, shot-level attempts, and episode budgets without network access:

```sh
python3 scripts/run_mock.py examples/episode.json --state work/run_state.json
```

## Seedance plan (explicit opt-in)

The adapter can inspect capabilities and construct a command without submitting. `--execute` is required for network generation; never use it without a provider budget and user approval.

```sh
python3 scripts/seedance_plan.py examples/episode.json --shot S01
```

## Subtitles and assembly plan

Generate an SRT and an encoder-independent clip plan without media encoding:

```sh
python3 scripts/make_srt.py examples/episode.json --out work/episode.srt
python3 scripts/assemble_plan.py examples/episode.json --out work/assembly.json
```

The plan is blocked until every expected shot file exists. It does not claim that a video was assembled.

For local encoder testing, generate disposable fixtures with `python3 scripts/fixture_episode.py --manifest examples/episode.json --out work/fixture`; fixture media is intentionally not committed.

Run the full offline delivery gate with `python3 scripts/offline_delivery.py examples/episode.json --out work/delivery`. It creates disposable shots, an assembly plan, a master MP4, SRT, and technical QA. A PASS is technical evidence only; it is not a story or platform approval.

## Human content review and publish approval

Approval records bind the content-review report and the exact files supplied with `--file`. Bind the final video, manifest, subtitle, technical QA, compliance report, and cover files; the delivery gate rejects a missing or changed required file. Reviewer/publisher names remain self-reported strings, not authenticated identities or signatures. Before real distribution, separately verify reviewer identity and platform compliance.

Record an actual human review in `qa_result.json` (repeat `--shot` for each reviewed shot):

```sh
python3 scripts/record_content_review.py --out work/delivery/qa_result.json --status PASS --reviewer "Name" --basis "All shots reviewed" --shot S01 --shot S02
```

Use `PENDING_HUMAN_REVIEW` until review is complete, or `FAIL` when it fails. This records the review; it does not inspect video or grant publish approval. Only after content review PASS and independently verified compliance PASS may an authorized publisher create the separate, hash-bound approval:

```sh
python3 scripts/approve_publish.py --qa work/delivery/qa_result.json --approved-by "Publisher" --basis "Release approved" --file work/delivery/master.mp4 --file examples/episode.json --file "work/delivery/制作成果/subs/The Signal_EP01.srt" --file work/delivery/technical_qa.json --file work/delivery/compliance_result.json
```

Changing `qa_result.json` or any bound file after approval invalidates that approval. The delivery manifest also requires technical QA PASS, compliance PASS, release metadata, subtitles, content review PASS, and separate human publish approval. Add one `--file` for each final cover or other release asset that the reviewer approved.

## Current boundaries

The bundled Seedance adapter requires explicit execution opt-in and is not a complete production integration: provider submission, polling, and download have not been validated against a real paid run in this repository. The documented audio-mode issue in `references/workflow.md` remains unresolved; do not treat the legacy audio mode as verified. This repository does not claim automated story review or platform approval. Legacy narrative and compliance keyword gates are advisory and use a different manifest contract. Do not use them to certify release readiness.

## Offline quick start

```sh
python3 scripts/validate_manifest.py examples/episode.json
python3 scripts/previz.py examples/episode.json --out work/previz.html
python3 scripts/estimate_cost.py examples/episode.json --rate 0.35 --pass-rate 0.65 --versions 3
python3 scripts/qa_report.py --manifest examples/episode.json --out work/qa.json
python3 -m unittest discover -s tests
```

`--rate` means currency units per generated second. Estimates exclude image, audio, tax and provider-specific charges. Keyword scanning does not establish platform compliance.

## Installation

Copy the complete repository into your agent's skill directory. Entry point: `SKILL.md`. Python 3.11+; the offline commands use the standard library.

## License

Apache-2.0; see LICENSE. No third-party director skill or proprietary media is bundled.

Community policy: see [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

Delivery status is intentionally staged: technical PASS does not equal content approval or publish approval.

## Naming and compatibility

The canonical product and skill name is **Yuanjing Storyforge / 元境·漫界工坊**. The repository was previously named `ai-comic-drama`; that phrase remains in keywords and history so existing search results and references remain discoverable. The Python import package is still `ai_comic_drama` and is not renamed in this release.
