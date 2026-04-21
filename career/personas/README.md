# Personas

## Purpose
Directory for modular persona files used by JT7.

## Rules
- `docs/persona-template.md` is the reusable base template.
- user-specific personas live in this directory.
- if a user persona has `active_for_runtime_context: yes`, runtime logic should prefer that file for user-specific context.
- if no user persona is active, fallback should be the template or other explicitly configured default.
