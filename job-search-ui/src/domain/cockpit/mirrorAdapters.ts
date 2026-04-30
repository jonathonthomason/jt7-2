import type { PriorityLevel } from './enums'
import type { MirrorRow, ReviewItem, ReviewProposedJobUpdate } from './types'

export function rowsToObjects(rows: string[][]): MirrorRow[] {
  const [header = [], ...data] = rows
  return data.map((row) => Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])))
}

function parseJson<T>(value: string, fallback: T): T {
  try {
    return value ? JSON.parse(value) as T : fallback
  } catch {
    return fallback
  }
}

function priorityFromReview(reason: string, confidence: number): PriorityLevel {
  if (reason.includes('interview') || confidence >= 0.75) return 'high'
  if (reason.includes('missing_company') || reason.includes('missing_role')) return 'medium'
  return 'low'
}

export function adaptReviewQueue(rows: string[][], signalRows: MirrorRow[]): ReviewItem[] {
  return rowsToObjects(rows).map((row) => {
    const linkedSignal = signalRows.find((signal) => signal.signal_id === row.signal_id)
    const proposed = parseJson<ReviewProposedJobUpdate>(row.proposed_job_update, {})
    const confidence = Number.parseFloat(row.confidence || '0') || 0
    return {
      id: row.review_id,
      signalId: row.signal_id,
      timestamp: row.timestamp,
      source: row.source,
      signalType: row.signal_type,
      extractedCompany: row.extracted_company,
      extractedRole: row.extracted_role,
      extractedRecruiter: row.extracted_recruiter,
      proposedAction: row.proposed_action,
      proposedJobUpdate: proposed,
      confidence,
      reasonForReview: row.reason_for_review,
      status: (row.status || 'pending') as ReviewItem['status'],
      resolutionNotes: row.resolution_notes || '',
      evidenceSummary: linkedSignal?.raw_excerpt || row.reason_for_review,
      linkedJobId: proposed.linkedJobId || proposed.linkedJobId || proposed.linkedJobId,
      linkedSignalSummary: linkedSignal?.raw_excerpt,
      priority: priorityFromReview(row.reason_for_review || '', confidence),
    }
  })
}
