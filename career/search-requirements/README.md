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
- `career/user_persona_reference.md` = upstream persona/profile source for targeting, fit context, and personalization
- `career/strategy.md` = strategic framing and positioning
- `career/search-requirements/*.md` = operational search constraints derived from persona/profile and active search decisions
- `career/pipeline.md` = tracked opportunities

## Rule
If a user-specific search requirements file exists and is active, JT7 should prefer it over generic assumptions.
If an active persona/profile reference exists, search requirements should be based on that persona/profile doc rather than stand-alone preference guesses.
Persona/profile should supply identity, positioning, role targeting, fit signals, and preference context; the search requirements layer should translate that into operational inclusion/exclusion criteria.
