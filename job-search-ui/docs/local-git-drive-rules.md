# Local Git Drive Rules

## Purpose
Keep all logic, modules, components, and data files aligned across local runtime, git, and Google Drive.

## Rules
- all runnable app logic lives locally in the workspace first
- all maintained app code should be committed to git
- important local app docs and modular reference files should be mirrored to Google Drive
- local runtime remains the execution surface
- git remains the versioned source of truth for code
- Google Drive remains the mirrored access and backup layer for selected code-adjacent docs and reference artifacts
- modules, components, mock data, and logic files should be structured so they can run locally without depending on Drive
- Drive copies must never become the only copy of important app logic or modular reference files
