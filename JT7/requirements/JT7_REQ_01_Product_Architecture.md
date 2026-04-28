# JT7 — Product Architecture

## Routes
/execute/today

/manage/jobs
/manage/recruiters
/manage/outreach
/manage/messages

/intelligence/competition
/intelligence/wiki
/intelligence/reports

/design-system/components
/design-system/foundations

/settings

## Global Shell
Persistent:
- Left nav
- Header
- Command bar
- Notifications
- Context switcher
- Optional right panel

## Behavior Rules
Navigation → changes workspace  
Right panel → inspect/edit object  
Command bar → execute/search  
Signals → feed Today’s Plan  

## Constraints
- No deep routing trees
- Avoid full page transitions
- Prefer inline + panel interactions