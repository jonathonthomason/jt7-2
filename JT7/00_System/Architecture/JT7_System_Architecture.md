# JT7 Job Intelligence System Architecture

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** foundational architecture
- **Status:** revised
- **Primary document path:** `JT7/00_System/Architecture/JT7_System_Architecture.md`
- **Primary canonical storage:** Google Drive
- **Execution note:** OpenClaw workspace is not an authoritative storage layer

## 1. System Objective
JT7 Job Intelligence System is a job intelligence and tracking system designed to coordinate job search data, logic, assets, and operational state across Google Drive, a local working mirror, a separate local recovery backup, Telegram, and external data sources.

> Consolidation note: this foundational architecture remains useful, but JT7's current consolidated MVP operating model now treats Google Sheets as the single operational source of truth for live tracker state, while Markdown documents remain architecture/governance/memory artifacts. Gmail, Calendar, and manual input are evidence inputs; runtime proof still depends on a verified execution surface.

The system must:
- use Google Drive as the canonical source of truth
- maintain a local JT7 working mirror for active local access and degraded-mode continuity
- maintain a separate local backup layer outside OpenClaw/workspace for recovery
- treat OpenClaw workspace as a non-authoritative execution environment
- separate structured data from system logic
- support future ingestion from email, job boards, and community systems
- remain usable by both humans and agents

## 2. Storage Hierarchy

## 2.1 Layer 1 — Canonical Source
- **Layer:** Google Drive
- **Role:** primary source of truth
- **Authority:** canonical
- **Purpose:** durable, shared, cross-device source for system logic, structured data, and operational artifacts

## 2.2 Layer 2 — Local Working Mirror
- **Layer:** local JT7 folder
- **Path root:** `~/JT7/`
- **Role:** secondary fallback and active local working copy
- **Authority:** non-canonical during normal online operation; temporary operating source during degraded mode
- **Purpose:** fast local access, degraded-mode continuity, local working copy of Drive artifacts

## 2.3 Layer 3 — Local Recovery Backup
- **Layer:** separate local backup folder outside OpenClaw/workspace
- **Role:** tertiary recovery backup
- **Authority:** recovery-only unless higher layers are unavailable
- **Purpose:** restore from corruption, local mirror failure, accidental deletion, or wider system failure

## 2.4 Non-Authoritative Runtime Layer
- **Layer:** OpenClaw workspace
- **Role:** execution and transformation layer
- **Authority:** non-authoritative
- **Purpose:** temporary reading, drafting, transforming, queueing, and agent runtime operations

### Runtime Rule
No long-term authoritative state should live only in the OpenClaw workspace.

## 3. Storage Model

### 3.1 Canonical Rule
- Google Drive is the source of truth when available
- local working mirror should reflect Drive state
- local backup exists for recovery, not as a normal operating authority
- OpenClaw workspace is disposable and reconstructable

### 3.2 Local Mirror Rule
- the local mirror is the active local copy of canonical artifacts
- it supports normal fast access and degraded-mode continuity
- it should maintain path parity with Drive where practical

### 3.3 Backup Rule
- the backup layer is distinct from the working mirror
- backups should be snapshot-oriented or version-preserving
- backup writes should never block successful Drive writes
- backup recovery should be explicit and auditable

## 4. Read / Write Priority Logic

## 4.1 Standard Online Mode
### Read priority
1. Google Drive
2. local working mirror
3. backup layer only for recovery inspection
4. OpenClaw workspace only if explicitly runtime-local

### Write priority
1. write to Google Drive
2. update local working mirror
3. update local backup snapshot layer
4. optionally update runtime copies if needed for immediate execution

### Online Write Rule
A successful Drive write is canonical even if mirror or backup update follows asynchronously.

## 4.2 Degraded / Temporary No-Drive Mode
### Trigger
Degraded mode is active when:
- Drive cannot be reached
- internet is unavailable
- Drive auth is temporarily invalid
- Drive write/read path is otherwise blocked

### Read priority
1. local working mirror
2. backup layer only if working mirror is unavailable or corrupt
3. runtime copy only as last temporary fallback

### Write behavior
1. write to local working mirror
2. create `pending_sync` marker
3. enqueue reconciliation back to Drive when available
4. optionally snapshot into backup layer if local policy requires it

### Degraded Mode Rule
Local mirror becomes the active operational layer temporarily, but canonical authority returns to Drive once sync is restored.

## 4.3 Recovery Mode
### Use recovery mode when
- Drive data is unavailable and local mirror is damaged
- local mirror is missing or corrupted
- a destructive error affects one or more layers

### Recovery order
1. restore from Drive if Drive is intact
2. restore from backup if Drive is unavailable or known bad
3. rebuild local mirror
4. rebuild runtime layer last

## 5. Backup Logic

## 5.1 Mirror vs Backup
### Local working mirror
- active local copy
- updated as part of normal operation
- supports degraded mode
- optimized for access and continuity

### Local backup
- recovery-oriented
- separate from working mirror
- preserves snapshots/versions
- not used as normal primary working copy

## 5.2 Snapshot / Version Behavior
Backups should preserve:
- file path
- snapshot time
- source layer
- version or revision marker when available

Preferred backup behavior:
- keep timestamped snapshots for critical files
- preserve older versions rather than destructive overwrite when feasible
- maintain enough history to recover from bad sync or corruption

## 5.3 Backup Location Rule
- backup must live outside the OpenClaw workspace
- backup should not depend on runtime-layer survival
- backup path should be stable and agent-readable when permitted

## 5.4 Backup Failure Rule
- backup failure must not block canonical Drive writes
- if backup update fails, mark backup status degraded and continue
- backup remediation can occur later without invalidating the Drive write

## 6. Offline / Degraded Mode

## 6.1 Degraded Mode Definition
Degraded mode is a real operating condition in which Drive is unavailable but local resources remain usable.

## 6.2 What Continues To Work
During degraded mode, the system should still support:
- local markdown docs
- local spreadsheets
- local instruction files
- local profile assets
- local research/reference assets
- local execution notes

## 6.3 What Gets Queued
During degraded mode, queue these for later sync or refresh:
- Drive sync operations
- email sync operations
- external site ingestion refreshes
- any external reconciliation requiring network access

## 6.4 Pending Sync Flags
Each locally changed artifact in degraded mode should support:
- `pending_sync: true | false`
- `last_local_write_at`
- `last_drive_sync_at`
- `sync_status: clean | pending | conflicted | failed`

## 6.5 Reconciliation Rules
When Drive returns:
1. identify all `pending_sync` artifacts
2. compare local mirror version with Drive version
3. if Drive unchanged since last sync, push local mirror to Drive
4. if both changed, mark conflict
5. do not silently overwrite semantic conflicts
6. update mirror and backup after reconciliation succeeds

## 7. Failure Scenarios

## 7.1 Drive Unavailable
- read from local mirror
- write locally
- mark `pending_sync`
- queue later reconciliation

## 7.2 Local Mirror Unavailable
- use Drive when online
- restore local mirror from Drive if possible
- if Drive unavailable too, restore from backup

## 7.3 Backup Unavailable
- continue with Drive + local mirror
- mark backup layer degraded
- repair backup later
- do not block canonical writes

## 7.4 OpenClaw Workspace Loss
- no authoritative state should be lost if Drive and local mirror are intact
- rebuild runtime layer from Drive/local mirror
- workspace should be treated as disposable

## 7.5 Partial Sync Failure
- mark affected artifacts as `failed` or `pending`
- preserve both known versions
- require explicit retry or reconciliation

## 7.6 Conflicting Versions Between Drive and Local
Conflict exists when:
- local mirror changed after `last_drive_sync_at`
- Drive changed after `last_drive_sync_at`
- semantic differences cannot be safely overwritten

Conflict resolution rules:
1. preserve both copies
2. compare timestamps and revision markers
3. inspect changed sections or structured fields
4. write explicit reconciliation result
5. update backup after resolved state is finalized

## 8. Artifact Classes

## 8.1 Structured Data
- **Purpose:** canonical tabular records for jobs, recruiters, companies, actions, and assets
- **Format:** spreadsheets
- **Canonical storage:** Google Drive in `01_Data/`
- **Working mirror:** `~/JT7/01_Data/`
- **Backup layer:** backup snapshot path outside workspace
- **Sync behavior:** Drive-first online, local-first in degraded mode, snapshot after stabilization

## 8.2 Instruction Logic
- **Purpose:** architecture, operating rules, prompts, workflows, contracts, protocols
- **Format:** Markdown
- **Canonical storage:** Google Drive in `00_System/`
- **Working mirror:** `~/JT7/00_System/`
- **Backup layer:** backup snapshot path outside workspace
- **Sync behavior:** same three-layer model; preserve semantic integrity during reconciliation

## 8.3 Identity / Profile
- **Purpose:** resume variants, positioning statements, bios, portfolio artifacts, persona/profile docs
- **Format:** Markdown, PDF, DOCX, text, related files
- **Canonical storage:** Google Drive in `02_Profile/`
- **Working mirror:** `~/JT7/02_Profile/`
- **Backup layer:** backup snapshot path outside workspace
- **Sync behavior:** version-sensitive, preserve history where practical

## 8.4 Reference Assets
- **Purpose:** job descriptions, company research, recruiter context, interview references, imported material
- **Format:** Markdown, PDF, HTML export, screenshots, docs, text
- **Canonical storage:** Google Drive in `03_Research/`
- **Working mirror:** `~/JT7/03_Research/`
- **Backup layer:** backup snapshot path outside workspace
- **Sync behavior:** append/import friendly, avoid destructive overwrite without comparison

## 8.5 Runtime / Queue
- **Purpose:** logs, queue items, sync records, transient runtime outputs
- **Format:** JSON, log text, Markdown, queue artifacts
- **Primary location:** local system, not canonical Drive by default
- **Typical paths:** local working mirror support folders and backup-support folders
- **Sync behavior:** local-first; only promote into canonical system if intentionally elevated

## 9. Folder Architecture

## 9.1 Google Drive Structure
```text
JT7/
 00_System/
   Architecture/
   Logic/
   Roadmap/
   Protocols/
 01_Data/
   Jobs/
   Recruiters/
   Companies/
   Actions/
   Assets/
 02_Profile/
   Resume/
   Positioning/
   Portfolio/
   Bio/
 03_Research/
   Job_Descriptions/
   Company_Research/
   Market/
   Community/
 04_Execution/
   Inbox/
   Working/
   Reviews/
 05_Archive/
   Snapshots/
   Deprecated/
   Historical/
```

## 9.2 Local Working Mirror Structure
```text
~/JT7/
 00_System/
   Architecture/
   Logic/
   Roadmap/
   Protocols/
 01_Data/
   Jobs/
   Recruiters/
   Companies/
   Actions/
   Assets/
 02_Profile/
   Resume/
   Positioning/
   Portfolio/
   Bio/
 03_Research/
   Job_Descriptions/
   Company_Research/
   Market/
   Community/
 04_Execution/
   Inbox/
   Working/
   Reviews/
 05_Archive/
   Snapshots/
   Deprecated/
   Historical/
 06_Logs/
 07_OfflineQueue/
```

## 9.3 Local Backup Structure
The backup layer should live outside the OpenClaw workspace and outside any temporary runtime directories.

Recommended root shape:
```text
<local-backup-root>/JT7_Backup/
 snapshots/
 manifests/
 recovery/
 logs/
```

### Backup intent
- `snapshots/` → timestamped or versioned artifact copies
- `manifests/` → what was backed up, from where, and when
- `recovery/` → staged restore operations
- `logs/` → backup/recovery event logs

## 10. System Roles

## 10.1 Google Drive
- canonical source of truth
- primary durable store
- primary write target in online mode
- authoritative source for human + agent collaboration

## 10.2 Local Working Mirror
- active local copy
- degraded-mode operating layer
- local read fallback
- local write target when Drive unavailable

## 10.3 Local Backup Folder
- tertiary recovery layer
- preserves snapshots and recovery history
- not primary working storage
- used for restoration when higher layers fail or become corrupt

## 10.4 OpenClaw Workspace
- execution and transformation layer
- temporary runtime workspace
- not authoritative
- safe to rebuild from authoritative layers

## 10.5 Telegram
- command and orchestration interface
- lightweight control surface
- capture and trigger layer
- not a storage system

## 10.6 Spreadsheets
- structured data layer
- canonical entity storage for jobs, recruiters, companies, actions, assets
- should contain normalized fields rather than operational prose

## 10.7 Markdown Docs
- instruction and logic layer
- architecture, contracts, prompts, protocols, and operating documents
- should be human-readable and agent-usable

## 10.8 External Systems
- source-input layer only at first
- examples: Gmail, job boards, communities, referrals, exports
- provide raw or semi-structured inputs to JT7
- do not replace JT7’s canonical storage layers

## 11. Source Priority and Version Logic

### 11.1 Authority Order
1. Google Drive
2. local working mirror
3. local backup
4. runtime workspace

### 11.2 Timestamp / Revision Fields
Durable artifacts should support where possible:
- `created_at`
- `updated_at`
- `last_synced_at`
- `source_origin: drive | local_mirror | backup | runtime`
- optional `version` or `revision`

### 11.3 Comparison Logic
- if only Drive changed after `last_synced_at`, Drive wins
- if only local mirror changed after `last_synced_at`, local mirror is eligible for Drive promotion
- if both changed after `last_synced_at`, mark conflict
- backup is not used to silently override Drive or mirror during normal operation; it is used to recover or compare

## 12. Design Principles
- **Single canonical authority:** Drive is authoritative when available
- **Layer separation:** canonical, mirror, backup, and runtime layers have distinct roles
- **Recoverability:** every important artifact should be restorable from more than one layer
- **Auditability:** sync, backup, and recovery states should be inspectable
- **Low cognitive load:** storage behavior should be simple and explicit
- **Explicit over implicit:** no hidden authority, no silent merges, no ambiguous recovery behavior
- **Runtime disposability:** execution environments should be rebuildable from authoritative stores
- **Degraded continuity:** important work should continue locally when Drive is unavailable

## 13. Current Implementation Strategy
Implementation should proceed in phases:
1. architecture
2. artifact inventory
3. schema/spec definitions
4. Drive/local mirror logic
5. backup snapshot layer
6. degraded mode later

### Implementation intent
- define storage and behavior first
- inventory real artifacts before automating movement
- implement mirror logic before recovery automation
- implement backup snapshot behavior before degraded-mode reconciliation complexity

## 14. Operating Rules
- do not write authoritative long-term state only into the OpenClaw workspace
- do not treat backup as the normal working source
- do not overwrite Drive from local mirror when conflict exists
- do not let backup failure block canonical Drive writes
- do not silently merge semantically meaningful markdown conflicts
- do not skip explicit `pending_sync` handling in degraded mode

## 15. Next Artifacts to Define
1. `JT7_Data_Model.md` — canonical entity definitions for jobs, recruiters, companies, actions, and assets
2. `JT7_Sync_Protocol.md` — sync rules, pending_sync handling, conflict resolution, and reconciliation flow
3. `JT7_Backup_and_Recovery_Spec.md` — backup snapshot behavior, restore logic, and recovery procedures
4. `JT7_Folder_Contracts.md` — folder-level purpose and artifact rules for every top-level directory and storage layer
5. `JT7_Input_Ingestion_Spec.md` — how Gmail, job boards, community sources, and manual imports become structured data
