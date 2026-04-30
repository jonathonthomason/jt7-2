import type { ReviewCommand, ReviewEventType } from './enums'
import type { ReviewEvent, ReviewItem, ReviewOutcomePayload } from './types'

function createReviewEvent(type: ReviewEventType, command: ReviewCommand, item: ReviewItem, payload?: ReviewOutcomePayload): ReviewEvent {
  return {
    id: `event_${item.id}_${Date.now()}`,
    reviewId: item.id,
    signalId: item.signalId,
    type,
    command,
    timestamp: new Date().toISOString(),
    actor: 'operator',
    notes: payload?.notes,
    linkedJobId: payload?.linkedJobId ?? item.proposedJobUpdate.linkedJobId,
  }
}

export const buildReviewConfirmedEvent = (item: ReviewItem, payload?: ReviewOutcomePayload) => createReviewEvent('review_confirmed', 'Confirm', item, payload)
export const buildReviewLinkedEvent = (item: ReviewItem, payload?: ReviewOutcomePayload) => createReviewEvent('review_linked', 'Link', item, payload)
export const buildReviewDismissedEvent = (item: ReviewItem, payload?: ReviewOutcomePayload) => createReviewEvent('review_dismissed', 'Dismiss', item, payload)
export const buildReviewDuplicateEvent = (item: ReviewItem, payload?: ReviewOutcomePayload) => createReviewEvent('review_duplicate', 'Mark Duplicate', item, payload)
export const buildReviewDeferredEvent = (item: ReviewItem, payload?: ReviewOutcomePayload) => createReviewEvent('review_deferred', 'Defer', item, payload)
export const buildReviewEscalatedEvent = (item: ReviewItem, payload?: ReviewOutcomePayload) => createReviewEvent('review_escalated', 'Escalate', item, payload)
