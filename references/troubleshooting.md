# Troubleshooting

## The offline quickstart fails

Run `python3 scripts/doctor.py` first. The offline workflow requires Python 3.11 or newer and does not require a provider CLI, credentials, ffmpeg, or network access. Run commands from the repository root so `scripts/` and `examples/` resolve correctly.

## `pip install .` fails

Use Python 3.11+ and upgrade the build tooling in the active environment if needed:

```sh
python3 -m pip install --upgrade pip setuptools
python3 -m pip install .
```

The package has no runtime dependencies. A provider CLI and ffmpeg are separate optional tools.

## Seedance says `blocked`

Submission is blocked unless the API client uses `SeedanceCLI(execute=True)`. The script `seedance_plan.py` only prints a plan and rejects `--execute`; it does not submit jobs. The adapter is opt-in and this release has no claim of a successful live paid run. Confirm the provider budget and account before enabling it.

## A Seedance submission is `unknown`

An unknown result means the local CLI timed out or returned no task ID. Do not submit the shot again automatically: the provider may already have accepted it. Check provider history, then resume polling with the original task ID if one is available.

## A download is `download_pending`

The task completed but the local artifact was not confirmed. Resume the same state file to retry the download. The runner does not create a new paid task for a download-only retry.

## Technical QA passes with a black-frame warning

`black_frame_detected_needs_review` is a warning from the current conservative detector. Inspect the actual video before content approval. Technical PASS does not certify story quality, platform compliance, or publication.

## Costs

Run `scripts/estimate_cost.py` with a provider price you have checked recently. The estimate is arithmetic only and excludes provider-specific fees, images, audio, tax, and any account quota rules.
