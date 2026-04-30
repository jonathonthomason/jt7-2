export const reviewStatuses = ['pending', 'confirmed', 'linked', 'dismissed', 'duplicate', 'deferred', 'escalated'] as const
export type ReviewStatus = (typeof reviewStatuses)[number]

export const reviewCommands = ['Confirm', 'Link', 'Dismiss', 'Mark Duplicate', 'Defer', 'Escalate'] as const
export type ReviewCommand = (typeof reviewCommands)[number]

export const opportunityStatuses = ['Found', 'Saved', 'Reviewing', 'Applied', 'Interviewing', 'Offer', 'Rejected', 'Archived', 'Cold', 'Recruiter Contacted'] as const
export type OpportunityStatus = (typeof opportunityStatuses)[number]

export const eventTypes = ['review_confirmed', 'review_linked', 'review_dismissed', 'review_duplicate', 'review_deferred', 'review_escalated'] as const
export type ReviewEventType = (typeof eventTypes)[number]

export const priorityLevels = ['critical', 'high', 'medium', 'low'] as const
export type PriorityLevel = (typeof priorityLevels)[number]
