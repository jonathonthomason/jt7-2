import { buildReviewConfirmedEvent, buildReviewDeferredEvent, buildReviewDismissedEvent, buildReviewDuplicateEvent, buildReviewEscalatedEvent, buildReviewLinkedEvent } from './eventBuilders'
import type { ReviewOutcomePayload, ReviewItem, ReviewEvent } from './types'

export type ReviewActionResult = {
  nextStatus: ReviewItem['status']
  event: ReviewEvent
}

export function confirmAsNewOpportunity(item: ReviewItem, payload?: ReviewOutcomePayload): ReviewActionResult {
  return { nextStatus: 'confirmed', event: buildReviewConfirmedEvent(item, payload) }
}

export function linkToExistingOpportunity(item: ReviewItem, payload?: ReviewOutcomePayload): ReviewActionResult {
  return { nextStatus: 'linked', event: buildReviewLinkedEvent(item, payload) }
}

export function dismissSignal(item: ReviewItem, payload?: ReviewOutcomePayload): ReviewActionResult {
  return { nextStatus: 'dismissed', event: buildReviewDismissedEvent(item, payload) }
}

export function markDuplicate(item: ReviewItem, payload?: ReviewOutcomePayload): ReviewActionResult {
  return { nextStatus: 'duplicate', event: buildReviewDuplicateEvent(item, payload) }
}

export function deferSignal(item: ReviewItem, payload?: ReviewOutcomePayload): ReviewActionResult {
  return { nextStatus: 'deferred', event: buildReviewDeferredEvent(item, payload) }
}

export function escalateSignal(item: ReviewItem, payload?: ReviewOutcomePayload): ReviewActionResult {
  return { nextStatus: 'escalated', event: buildReviewEscalatedEvent(item, payload) }
}
