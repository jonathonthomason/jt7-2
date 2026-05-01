import type { OpportunityStatus, PriorityLevel, ReviewCommand, ReviewEventType, ReviewStatus } from './enums'

export type StagingFitBand = 'strong' | 'maybe' | 'weak'
export type StagingDecision = 'pending' | 'promote' | 'hold' | 'reject'

export type MirrorRow = Record<string, string>

export type ReviewProposedJobUpdate = {
  linkedJobId?: string
  proposedStatus?: OpportunityStatus | string
  company?: string
  role?: string
}

export type ReviewItem = {
  id: string
  signalId: string
  timestamp: string
  source: string
  signalType: string
  extractedCompany: string
  extractedRole: string
  extractedRecruiter: string
  proposedAction: string
  proposedJobUpdate: ReviewProposedJobUpdate
  confidence: number
  reasonForReview: string
  status: ReviewStatus
  resolutionNotes: string
  evidenceSummary: string
  linkedJobId?: string
  linkedSignalSummary?: string
  priority: PriorityLevel
}

export type ReviewOutcomePayload = {
  notes?: string
  linkedJobId?: string
}

export type ReviewEvent = {
  id: string
  reviewId: string
  signalId: string
  type: ReviewEventType
  command: ReviewCommand
  timestamp: string
  actor: string
  notes?: string
  linkedJobId?: string
}

export type StagedOpportunity = {
  id: string
  canonicalJobId?: string
  company: string
  role: string
  location: string
  source: string
  sourceBoard: string
  boardJobId?: string
  provenance: string
  status: StagingDecision
  trustLevel: 'staged' | 'reviewed'
  fitBand: StagingFitBand
  duplicateRisk: 'low' | 'medium' | 'high'
  recommendedAction: string
  reasons: string[]
  link?: string
  notes?: string
}
