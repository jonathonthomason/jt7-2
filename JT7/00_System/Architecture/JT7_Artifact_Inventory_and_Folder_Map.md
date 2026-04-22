# JT7 Artifact Inventory and Folder Map

## Document Metadata
- **System:** JT7 Job Intelligence System
- **Document type:** master artifact inventory and folder map
- **Status:** draft-initial
- **Primary path:** `JT7/00_System/Architecture/JT7_Artifact_Inventory_and_Folder_Map.md`
- **Purpose:** define what artifacts the system manages, where they belong, what formats they use, and how they should be handled across canonical, mirror, runtime, and backup layers

## 1. Document Role
> Consolidation note: this artifact map remains useful, but JT7's current MVP operating model now distinguishes more sharply between live tracker truth (Google Sheets), evidence inputs (Gmail, Calendar, manual), and markdown architecture/governance artifacts. Until rewritten, treat this document as partially legacy where it implies a broader or more distributed operational truth model than the current MVP governance rules.

This document defines the operational artifact map for JT7.
It does not redefine system architecture.
It defines:
- artifact classes
- sub-artifacts
- folder placement
- handling rules
- versioning expectations
- relationships to Telegram, OpenClaw, spreadsheets, markdown, and external systems

## 2. Artifact Classes

## 2.1 Structured Data
- **Purpose:** canonical structured records used by the system for tracking, querying, filtering, and reporting
- **Common formats:** Google Sheets, XLSX import sources, CSV export/import, tabular local copies
- **Canonical location:** `JT7/01_Data/`
- **Local mirror:** `~/JT7/01_Data/`
- **Backup behavior:** snapshot into `~/JT7_backup/01_Data/` and backup snapshots area
- **Examples:** jobs tracker, recruiters tracker, communications tracker, competition tracker, lookup tables, rollup dashboards

## 2.2 Instruction Logic
- **Purpose:** define system rules, schemas, prompts, protocols, naming rules, and operating contracts
- **Common formats:** Markdown
- **Canonical location:** `JT7/00_System/`
- **Local mirror:** `~/JT7/00_System/`
- **Backup behavior:** snapshot into `~/JT7_backup/00_System/`
- **Examples:** system architecture, sync rules, data specs, Telegram command model, degraded-mode rules, recovery playbook

## 2.3 Identity / Profile
- **Purpose:** store job-search identity artifacts, positioning materials, resumes, messaging assets, and profile documentation
- **Common formats:** Markdown, PDF, DOCX, TXT
- **Canonical location:** `JT7/02_Profile/`
- **Local mirror:** `~/JT7/02_Profile/`
- **Backup behavior:** snapshot into `~/JT7_backup/02_Profile/`
- **Examples:** master resume, tailored resumes, persona/positioning docs, market profile, messaging templates, portfolio summaries

## 2.4 Research / Reference
- **Purpose:** hold imported, saved, or curated research and reference artifacts used to support decisions and execution
- **Common formats:** Markdown, PDF, TXT, HTML export, images/screenshots, DOCX
- **Canonical location:** `JT7/03_Research/`
- **Local mirror:** `~/JT7/03_Research/`
- **Backup behavior:** snapshot into `~/JT7_backup/03_Research/`
- **Examples:** saved job descriptions, recruiter screenshots, company research, interview notes, market signal notes, community leads

## 2.5 Runtime / Queue / Logs
- **Purpose:** support operational execution, sync, import, review, and audit trails
- **Common formats:** JSON, Markdown, log text, queue records
- **Canonical location:** mixed; mostly non-canonical operational layer
- **Local mirror:** `~/JT7/04_Execution/`, `~/JT7/06_Logs/`, `~/JT7/07_OfflineQueue/`
- **Backup behavior:** selective backup only for operationally important items
- **Examples:** pending sync queue, ingestion queue, failed ingestion log, manual review queue, command history, change log, operational notes

## 2.6 Backup / Archive
- **Purpose:** preserve historical states, recovery points, deprecated assets, and replaced artifacts
- **Common formats:** same as source artifacts, plus manifests/logs
- **Canonical location:** `JT7/05_Archive/`
- **Local mirror:** `~/JT7/05_Archive/`
- **Backup behavior:** `~/JT7_backup/05_Archive/` and `~/JT7_backup/snapshots/`
- **Examples:** dated snapshots, archived spreadsheets, archived specs, deprecated docs, recovery points

## 3. Sub-Artifact Inventory

## 3.1 Structured Data Sub-Artifacts

### Jobs tracker
- **Purpose:** canonical list of roles/opportunities
- **Preferred format:** spreadsheet
- **Canonical location:** `JT7/01_Data/Jobs/`
- **Mirror:** `~/JT7/01_Data/Jobs/`
- **Backup:** `~/JT7_backup/01_Data/Jobs/`

### Recruiters tracker
- **Purpose:** canonical contact records for recruiters, hiring managers, referrers
- **Preferred format:** spreadsheet
- **Canonical location:** `JT7/01_Data/Recruiters/`
- **Mirror:** `~/JT7/01_Data/Recruiters/`
- **Backup:** `~/JT7_backup/01_Data/Recruiters/`

### Communications tracker
- **Purpose:** communication events tied to recruiters, jobs, companies, and next actions
- **Preferred format:** spreadsheet
- **Canonical location:** `JT7/01_Data/Communications/`
- **Mirror:** `~/JT7/01_Data/Communications/`
- **Backup:** `~/JT7_backup/01_Data/Communications/`

### Competition tracker
- **Purpose:** track peer candidates, role competition assumptions, market/competition signals, or company competitive context depending on chosen model
- **Preferred format:** spreadsheet
- **Canonical location:** `JT7/01_Data/Competition/`
- **Mirror:** `~/JT7/01_Data/Competition/`
- **Backup:** `~/JT7_backup/01_Data/Competition/`

### Lookup / controlled values
- **Purpose:** normalize statuses, sources, channels, location types, pipeline stages, tags, and categorical values
- **Preferred format:** spreadsheet or lightweight markdown contract
- **Canonical location:** `JT7/01_Data/Lookups/`
- **Mirror:** `~/JT7/01_Data/Lookups/`
- **Backup:** `~/JT7_backup/01_Data/Lookups/`

### Optional future rollup dashboards
- **Purpose:** derived reporting surfaces for counts, summaries, trends, and workload views
- **Preferred format:** spreadsheet tabs or derived markdown summaries
- **Canonical location:** `JT7/01_Data/Dashboards/`
- **Mirror:** `~/JT7/01_Data/Dashboards/`
- **Backup:** `~/JT7_backup/01_Data/Dashboards/`

## 3.2 Instruction Logic Sub-Artifacts

### System architecture
- **Canonical location:** `JT7/00_System/Architecture/`
- **Format:** Markdown

### Storage and sync rules
- **Canonical location:** `JT7/00_System/Logic/`
- **Format:** Markdown

### Jobs data spec
- **Canonical location:** `JT7/00_System/Logic/Data_Specs/`
- **Format:** Markdown

### Recruiters data spec
- **Canonical location:** `JT7/00_System/Logic/Data_Specs/`
- **Format:** Markdown

### Communications data spec
- **Canonical location:** `JT7/00_System/Logic/Data_Specs/`
- **Format:** Markdown

### Competition data spec
- **Canonical location:** `JT7/00_System/Logic/Data_Specs/`
- **Format:** Markdown

### Telegram command model
- **Canonical location:** `JT7/00_System/Protocols/`
- **Format:** Markdown

### Offline / degraded mode rules
- **Canonical location:** `JT7/00_System/Protocols/`
- **Format:** Markdown

### Recovery playbook
- **Canonical location:** `JT7/00_System/Protocols/`
- **Format:** Markdown

### Naming conventions
- **Canonical location:** `JT7/00_System/Standards/`
- **Format:** Markdown

### File/folder standards
- **Canonical location:** `JT7/00_System/Standards/`
- **Format:** Markdown

## 3.3 Identity / Profile Sub-Artifacts

### Master resume
- **Canonical location:** `JT7/02_Profile/Resume/`
- **Format:** Markdown source + export formats if needed

### Tailored resumes
- **Canonical location:** `JT7/02_Profile/Resume/Tailored/`
- **Format:** Markdown, DOCX, PDF

### Persona / positioning docs
- **Canonical location:** `JT7/02_Profile/Positioning/`
- **Format:** Markdown

### Demographics / market profile
- **Canonical location:** `JT7/02_Profile/Market_Profile/`
- **Format:** Markdown or spreadsheet if structured

### Messaging templates
- **Canonical location:** `JT7/02_Profile/Messaging/`
- **Format:** Markdown

### Bio / summary docs
- **Canonical location:** `JT7/02_Profile/Bio/`
- **Format:** Markdown, TXT

### Portfolio notes / project summaries
- **Canonical location:** `JT7/02_Profile/Portfolio/`
- **Format:** Markdown, PDF, DOCX

## 3.4 Research / Reference Sub-Artifacts

### Saved job descriptions
- **Canonical location:** `JT7/03_Research/Job_Descriptions/`
- **Format:** PDF, HTML export, Markdown, TXT

### Recruiter screenshots
- **Canonical location:** `JT7/03_Research/Recruiter_Screenshots/`
- **Format:** PNG, JPG, PDF

### Company research
- **Canonical location:** `JT7/03_Research/Company_Research/`
- **Format:** Markdown, PDF, DOCX, TXT

### Interview notes
- **Canonical location:** `JT7/03_Research/Interview_Notes/`
- **Format:** Markdown, TXT

### Market signal notes
- **Canonical location:** `JT7/03_Research/Market_Signals/`
- **Format:** Markdown

### Community-sourced leads
- **Canonical location:** `JT7/03_Research/Community_Leads/`
- **Format:** Markdown, spreadsheet, TXT

### External source snapshots
- **Canonical location:** `JT7/03_Research/External_Snapshots/`
- **Format:** HTML export, PDF, screenshot, Markdown summary

## 3.5 Runtime / Queue / Logs Sub-Artifacts

### Pending sync queue
- **Location:** `~/JT7/07_OfflineQueue/`
- **Format:** JSON or Markdown queue records

### External ingestion queue
- **Location:** `~/JT7/04_Execution/Queues/`
- **Format:** JSON / Markdown records

### Failed ingestion log
- **Location:** `~/JT7/06_Logs/`
- **Format:** log text / JSON / Markdown

### Manual review queue
- **Location:** `~/JT7/04_Execution/Manual_Review/`
- **Format:** Markdown or spreadsheet

### Command history
- **Location:** `~/JT7/06_Logs/`
- **Format:** log text / Markdown

### Change log
- **Location:** `~/JT7/04_Execution/Change_Log/`
- **Format:** Markdown

### Operational notes
- **Location:** `~/JT7/04_Execution/Operational_Notes/`
- **Format:** Markdown

## 3.6 Backup / Archive Sub-Artifacts

### Dated snapshot backups
- **Location:** `~/JT7_backup/snapshots/`
- **Format:** source artifact formats plus manifest references

### Archived spreadsheets
- **Canonical archive location:** `JT7/05_Archive/Structured_Data/`
- **Mirror:** `~/JT7/05_Archive/Structured_Data/`
- **Backup:** `~/JT7_backup/05_Archive/Structured_Data/`

### Archived markdown specs
- **Canonical archive location:** `JT7/05_Archive/Specs/`
- **Mirror:** `~/JT7/05_Archive/Specs/`
- **Backup:** `~/JT7_backup/05_Archive/Specs/`

### Deprecated docs
- **Canonical archive location:** `JT7/05_Archive/Deprecated/`
- **Mirror:** `~/JT7/05_Archive/Deprecated/`
- **Backup:** `~/JT7_backup/05_Archive/Deprecated/`

### Recovery points
- **Location:** `~/JT7_backup/recovery/`
- **Format:** manifests, snapshot references, restore notes

## 4. Folder Map

## 4.1 Google Drive Canonical Layer
```text
JT7/
 00_System/
   Architecture/
   Logic/
    Data_Specs/
   Protocols/
   Standards/
   Roadmap/
 01_Data/
   Jobs/
   Recruiters/
   Communications/
   Competition/
   Lookups/
   Dashboards/
 02_Profile/
   Resume/
    Tailored/
   Positioning/
   Market_Profile/
   Messaging/
   Bio/
   Portfolio/
 03_Research/
   Job_Descriptions/
   Recruiter_Screenshots/
   Company_Research/
   Interview_Notes/
   Market_Signals/
   Community_Leads/
   External_Snapshots/
 04_Execution/
   Inbox/
   Working/
   Reviews/
 05_Archive/
   Structured_Data/
   Specs/
   Deprecated/
   Historical/
```

### Layer rule
- canonical folders live here
- authoritative business/system truth lives here unless explicitly runtime-only

## 4.2 Local Working Mirror
```text
~/JT7/
 00_System/
   Architecture/
   Logic/
    Data_Specs/
   Protocols/
   Standards/
   Roadmap/
 01_Data/
   Jobs/
   Recruiters/
   Communications/
   Competition/
   Lookups/
   Dashboards/
 02_Profile/
   Resume/
    Tailored/
   Positioning/
   Market_Profile/
   Messaging/
   Bio/
   Portfolio/
 03_Research/
   Job_Descriptions/
   Recruiter_Screenshots/
   Company_Research/
   Interview_Notes/
   Market_Signals/
   Community_Leads/
   External_Snapshots/
 04_Execution/
   Inbox/
   Working/
   Reviews/
   Queues/
   Manual_Review/
   Change_Log/
   Operational_Notes/
 05_Archive/
   Structured_Data/
   Specs/
   Deprecated/
   Historical/
 06_Logs/
 07_OfflineQueue/
```

### Layer rule
- mirrored from Drive for canonical artifacts
- also contains local-only operational folders such as logs and offline queue

## 4.3 Local Recovery Backup
```text
~/JT7_backup/
 00_System/
 01_Data/
 02_Profile/
 03_Research/
 04_Execution/
 05_Archive/
 snapshots/
 manifests/
 recovery/
 logs/
```

### Layer rule
- backup-only or recovery-oriented
- not normal working storage
- used for restore and historical protection

## 4.4 Folder Type Classification
### Canonical
- Drive folders under `JT7/00_System/` through `JT7/05_Archive/`

### Mirrored
- corresponding folders under `~/JT7/00_System/` through `~/JT7/05_Archive/`

### Runtime-only
- `~/JT7/04_Execution/Queues/`
- `~/JT7/04_Execution/Manual_Review/`
- `~/JT7/04_Execution/Change_Log/`
- `~/JT7/04_Execution/Operational_Notes/`
- `~/JT7/06_Logs/`
- `~/JT7/07_OfflineQueue/`

### Backup-only
- `~/JT7_backup/snapshots/`
- `~/JT7_backup/manifests/`
- `~/JT7_backup/recovery/`
- `~/JT7_backup/logs/`

## 5. File Handling Rules

## 5.1 Structured Data
- **Preferred format:** spreadsheet
- **Manual edit:** yes
- **Agent-readable:** yes
- **Mirror locally:** yes
- **Snapshot:** yes
- **Regenerable:** partially; schema yes, real data no
- **High-risk if lost:** yes

## 5.2 Instruction Logic
- **Preferred format:** Markdown
- **Manual edit:** yes
- **Agent-readable:** yes
- **Mirror locally:** yes
- **Snapshot:** yes
- **Regenerable:** partially, but loss is high-risk because logic drift matters
- **High-risk if lost:** yes

## 5.3 Resumes / Profile Docs
- **Preferred format:** Markdown source plus exportable document formats where needed
- **Manual edit:** yes
- **Agent-readable:** yes
- **Mirror locally:** yes
- **Snapshot:** yes
- **Regenerable:** partially, but not safely assumed
- **High-risk if lost:** yes

## 5.4 Research Assets
- **Preferred format:** source-native plus Markdown summaries where helpful
- **Manual edit:** usually yes for summaries, no for raw captures
- **Agent-readable:** yes if text-based; limited for binary assets unless OCR/export exists
- **Mirror locally:** yes
- **Snapshot:** selective for critical artifacts
- **Regenerable:** sometimes, but not guaranteed
- **High-risk if lost:** medium to high depending on rarity/source

## 5.5 Runtime / Queue / Logs
- **Preferred format:** JSON, log text, Markdown
- **Manual edit:** minimal; only if operationally necessary
- **Agent-readable:** yes
- **Mirror locally:** local-primary
- **Snapshot:** selective
- **Regenerable:** often yes, but queue state may matter
- **High-risk if lost:** medium; some queue state can be important

## 5.6 Backup / Archive
- **Preferred format:** original source formats plus manifests
- **Manual edit:** generally no except restore/recovery notes
- **Agent-readable:** yes
- **Mirror locally:** backup is already local
- **Snapshot:** yes by definition
- **Regenerable:** no, because this layer exists to preserve historical states
- **High-risk if lost:** high for recovery posture

## 6. Versioning Expectations

## 6.1 Markdown Documents
- use stable canonical filenames
- include document metadata header where useful
- when replaced materially, archive prior version to archive or backup snapshot
- avoid proliferating near-duplicate filenames unless they represent meaningful variants

## 6.2 Spreadsheets
- maintain stable canonical file names for active trackers
- prefer archived dated copies when structure changes materially
- preserve lookup/value definitions separately from working data when possible

## 6.3 Resumes / Profile Docs
- keep one master canonical source
- keep tailored variants in a dedicated folder
- archive obsolete variants instead of overwriting without trace
- use clear naming with role/company/date where appropriate

## 6.4 Research Assets
- preserve source-native filenames when imported if they contain useful provenance
- add dated snapshots or archive copies for critical references
- prefer summary companion docs over editing raw imported files

## 6.5 Backups / Snapshots
- use dated snapshots
- maintain manifests for what was captured and from which layer
- recovery points should be explicit and inspectable

## 7. Artifact Relationships to System Surfaces

## 7.1 Telegram
Telegram should:
- trigger capture and orchestration actions
- initiate updates to structured data and instruction logic
- request reads from canonical or mirrored layers
- not act as durable storage

### Typical artifact effects
- create/update tracker rows
- add operational notes
- trigger spec lookups
- trigger queue entries

## 7.2 OpenClaw Runtime
OpenClaw should:
- read from Drive or local mirror depending on availability
- write through to canonical or degraded-mode local paths
- use workspace for execution only
- never become the sole authoritative layer

## 7.3 External Systems
External systems should feed:
- structured data imports
- research/reference artifacts
- runtime ingestion queues
- future communications or company/job updates

Examples:
- Gmail → communications, recruiters, jobs
- job boards → jobs, companies, research snapshots
- communities → leads, recruiter context, research notes

## 7.4 Spreadsheets vs Markdown Truth
### Spreadsheets should hold
- structured entity records
- controlled values
- operational lists
- tracker state

### Markdown should hold
- architecture
- specs
- rules
- prompts
- operating protocols
- narrative or explanatory logic

## 8. Priority Artifacts to Build First
1. jobs tracker schema and file contract
2. recruiters tracker schema and file contract
3. communications tracker schema and file contract
4. competition tracker schema and file contract
5. lookup / controlled values spec
6. storage and sync rules document
7. Telegram command model
8. offline / degraded mode rules
9. recovery playbook
10. file/folder standards and naming conventions
