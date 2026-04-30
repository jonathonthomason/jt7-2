# Search Requirements

## Purpose
This directory holds modular job-search requirement files.

Use this layer for search constraints that should drive sourcing, filtering, and fit decisions.
Examples:
- target role set
- allowed locations
- remote / hybrid / onsite rules
- seniority targets
- deprioritized roles
- fit filters
- company preferences

## Structure
- one file per job seeker
- each file should be runtime-friendly and easy to parse later
- each file should declare whether it is the canonical active search requirements file

## Naming
Preferred pattern:
- `<persona-id>.md`

Example:
- `jonathon-thomason.md`

## Relationship to Other Files
- `career/strategy.md` = strategic framing and positioning
- `career/search-requirements/*.md` = operational search constraints
- `career/pipeline.md` = tracked opportunities

## Rule
If a user-specific search requirements file exists and is active, JT7 should prefer it over generic assumptions.
