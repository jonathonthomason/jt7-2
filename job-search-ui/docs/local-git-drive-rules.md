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
- tracker CRUD must synchronize across Google Sheets, local mirror state, and git-tracked local files
- Google Sheets is the live tracker truth; local and git are synchronized mirrors of tracker state
- scheduled JT7 runtime passes must enforce the Sheets -> local mirror -> git sequence on meaningful tracker changes
- Gmail-driven tracker updates must follow the same Sheets -> local mirror -> git sequence
- TaskRuns updates count as meaningful tracker writes and must be included before local mirror sync
- when no meaningful tracker CRUD happened, runtime reporting must explicitly say so and may skip mirror/git only if no tracked local files changed
- runtime reports under `job-search-ui/runtime/reports/` and tracker mirror files under `job-search-ui/data_mirror/` are part of the synchronized persistence layer and should be committed when changed
- Google Drive mirrors should be refreshed for important runtime rules/docs when execution behavior materially changes
