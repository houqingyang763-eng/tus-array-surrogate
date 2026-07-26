# JASACode_FEUNet reproducibility audit

This directory audits the author-provided artifact for:

`Finite difference-embedded UNet for solving transcranial ultrasound frequency-domain wavefield`

## Scope

- Verify the Figshare record and archive integrity.
- Inventory source code, data, checkpoints, environments, and runnable entrypoints.
- Compare implemented inputs, outputs, losses, and experiments with the paper.
- Attempt the smallest source-faithful run only after the user explicitly approves execution.

This audit does not adapt FEUNet to 3D, variable element geometry, or the current project task. It also does not inspect or reproduce Neuroseismic.

## Evidence rule

Claims are classified as:

- `verified`: directly inspected or executed in this audit.
- `reported`: stated by the paper or artifact metadata but not reproduced here.
- `unknown`: not established by available material.

See `AUDIT_LOG.md` for the running record and final reproducibility judgment.

## Resumable artifact download

`resume_download.ps1` works around Figshare's short-lived S3 download URLs. It
uses one stable connection and starts a fresh signed-URL attempt whenever that
connection expires. Completion requires both the official byte count and MD5.

```powershell
powershell -ExecutionPolicy Bypass -File experiments\feunet_repro_audit\resume_download.ps1
```

Large files are stored outside the C: repository at:

`D:\tus-array-surrogate-experiments\feunet_repro_audit\`

The C: repository contains only the audit notes and helper script. The helper
script also defaults to the D: artifact directory.
