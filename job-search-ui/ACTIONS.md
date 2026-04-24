# ACTIONS.md

## Purpose
Defines the canonical JT7 Actions contract for Phase 3A.

## Canonical states
- open
- waiting
- done
- blocked

## Rules
- Actions must trace back to Signals.
- Actions should link to Jobs when a valid job exists.
- Review-blocked items should persist as blocked actions rather than vanish.
- Today's Plan should be rebuildable from Actions + Signals + Jobs.
