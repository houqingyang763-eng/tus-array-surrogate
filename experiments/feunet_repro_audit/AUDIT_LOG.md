# JASACode_FEUNet audit log

## Audit target

- Paper DOI: `10.1121/10.0025391`
- Artifact title: `JASACode_FEUNet`
- Figshare DOI: `10.6084/m9.figshare.25117025.v1`
- Figshare article ID: `25117025`
- Published: `2024-01-31`
- Artifact file: `JASACode.rar`
- Reported archive size: `16,087,955,914 bytes`
- Direct file ID: `44328011`

## Reproducibility question

Does the author artifact contain enough source, data, configuration, and instructions to reproduce at least one paper-aligned FEUNet result without inventing missing scientific method details?

## Acceptance levels

- `R0 metadata only`: artifact exists, but code cannot be inspected.
- `R1 inspectable`: source and data structure can be inventoried.
- `R2 runnable inference`: an author-supplied model or configuration produces a paper-aligned output.
- `R3 runnable training`: an author-supplied training path runs on supplied or author-generated data.
- `R4 result reproduction`: at least one reported metric or figure is reproduced within a stated tolerance.

## Running log

### 2026-07-21 - Audit initialized

- `verified`: The audit is isolated under `experiments/feunet_repro_audit/`.
- `verified`: C: had approximately 55.7 GB free before artifact download.
- `verified`: The Figshare API exposes one RAR file of approximately 16.1 GB.
- `pending`: Obtain the archive inventory before full extraction.
- `pending`: Record hashes, unpacked size, code entrypoints, dependencies, data, and checkpoints.
- `pending`: Attempt a source-faithful minimal run.

### 2026-07-21 - Download failure diagnosed and guarded resume added

- `verified`: Sixteen parallel connections triggered repeated HTTP `502`
  responses from the Figshare redirect endpoint.
- `verified`: The surviving S3 URL contained `X-Amz-Expires=10`; after its
  connection ended, reuse of that expired URL produced HTTP `403`.
- `verified`: The partial RAR and aria2 control file remained resumable.
- `implemented`: `resume_download.ps1` now uses one connection and launches a
  fresh Figshare request after each failed transfer, with increasing delay when
  no bytes are gained.
- `implemented`: Download completion requires exactly `16,087,955,914` bytes
  and MD5 `0b737a28fbbb2843eb63ee07c78fd302`.
- `verified`: A forced termination of the inner aria2 process was detected;
  the watchdog waited 10 seconds, requested a fresh signed URL, and restarted
  aria2 without losing the partial archive.
- `implemented`: Connections remaining below `128 KiB/s` are treated as stale
  after the configured timeout and refreshed automatically.

### 2026-07-21 - Download completed and static package audit

- `verified`: Archive size is `16,087,955,914 bytes`; MD5 is
  `0b737a28fbbb2843eb63ee07c78fd302`, matching Figshare.
- `verified`: The archive and all large audit artifacts were moved to
  `D:\tus-array-surrogate-experiments\feunet_repro_audit\`. The C: repository
  now retains only small notes and scripts.
- `verified`: The RAR contains 408 entries and about 15.189 GiB uncompressed.
  It includes 256 training samples, 100 testing samples, two model-weight
  files, precomputed predictions/errors/losses, one short README, and one
  MATLAB visualization script.
- `verified`: There are no original `.py` files, dependency lock files, or
  data-generation scripts. The four train/test entrypoints are 64-bit Linux
  PyInstaller executables of about 3.699 GiB each.
- `verified`: The executables embed Python 3.7 and PyTorch `1.8.2+cu111`.
  Their small application entry bytecode was extracted and decompiled for
  static reading only. These decompiled files are audit reconstructions, not
  author-published source and not yet runnable reproductions.
- `verified`: Both baselines use the same 2D U-Net: one `151 x 151` input
  channel, encoder widths `8, 16, 32, 64, 128`, skip connections, and two
  `151 x 151` output channels for real and imaginary wavefield components.
- `verified`: Each sample stores `vsample` as a real `151 x 151` medium map
  and `wsample` as a complex `151 x 151` frequency-domain wavefield. The
  source distribution is a single shared `Ps_2D.mat`, not a variable network
  input.
- `verified`: Training constants in the recovered entry are 150 kHz, 2 mm
  grid spacing, 1500 epochs, batch size 16, Adam learning rate 0.001. FEUNet
  adds real/imaginary finite-difference Helmholtz residual losses at 546
  coordinates with weight 10; plain UNet uses only field MSE.
- `verified`: The package includes pretrained weights for both FEUNet and
  plain UNet, but its README gives no package versions, installation steps,
  hardware requirements, random seed, or command examples beyond naming the
  four executables.
- `static concern`: The recovered FEUNet training entry applies its physics
  loop as `for ii in range(1)` despite batch size 16. This appears to evaluate
  the physics residual for only the first sample in each batch, but must be
  checked against original source before treating it as a confirmed paper bug.
- `not attempted`: No author executable, model inference, training, or result
  reproduction was run, following the user's instruction.

## Final judgment

Status: `R1 static inspection achieved; R2-R4 not attempted`

The package is much stronger than metadata-only because it supplies data,
weights, results, and runnable Linux bundles. It is not a conventional
source-code release: the original readable network/training source and full
environment instructions are absent. A faithful source-level reproduction
therefore still requires reconstruction and later execution checks.
