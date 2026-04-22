# Mock Data Rules

## Purpose
Defines how app mock data and related logic should stay modular and contextualized from markdown-guided system logic.

## Rules
- mock data should remain replaceable and isolated from UI components
- fixture structure should reflect modular domain entities
- persona, routing, and app behavior rules should stay documented in markdown files outside component code
- UI should consume API-shaped data, not hardcoded presentation-only values
- if domain logic changes materially, update the related markdown rule file before expanding fixture behavior

## Current linked markdown context
- `../docs/persona-template.md`
- `../career/personas/jonathon-thomason.md`
- `../docs/storage-rules.md`
