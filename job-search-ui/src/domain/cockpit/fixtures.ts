import type { ReviewItem } from './types'

export function buildFallbackReviewSelection(items: ReviewItem[]): ReviewItem[] {
  if (items.length) return items
  return [
    {
      id: 'review_fallback_001',
      signalId: 'signal_fallback_001',
      timestamp: new Date().toISOString(),
      source: 'local',
      signalType: 'unknown_review_needed',
      extractedCompany: 'Example Co',
      extractedRole: 'Senior Product Designer',
      extractedRecruiter: 'recruiter_001',
      proposedAction: 'Review signal manually',
      proposedJobUpdate: { company: 'Example Co', role: 'Senior Product Designer', proposedStatus: 'Reviewing' },
      confidence: 0.42,
      reasonForReview: 'fallback preview item',
      status: 'pending',
      resolutionNotes: '',
      evidenceSummary: 'Fallback item generated because ReviewQueue mirror was empty.',
      priority: 'medium',
    },
  ]
}
