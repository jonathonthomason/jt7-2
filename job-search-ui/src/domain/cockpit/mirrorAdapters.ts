import type { PriorityLevel } from './enums'
import type { MirrorRow, ReviewItem, ReviewProposedJobUpdate, StagedOpportunity, StagingFitBand } from './types'

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

function fitBandFor(role: string, location: string): StagingFitBand {
  const roleText = role.toLowerCase()
  const locationText = location.toLowerCase()
  const seniorMatch = ['principal product designer', 'lead product designer', 'staff product designer', 'senior product designer'].some((token) => roleText.includes(token))
  const dfwMatch = ['dallas', 'fort worth', 'dfw', 'plano', 'irving', 'frisco', 'addison', 'arlington', 'richardson', 'grapevine'].some((token) => locationText.includes(token))
  const remoteMatch = locationText.includes('remote')
  const weakSignals = ['design system', 'mobile', 'visual', 'brand', 'ux/ui'].some((token) => roleText.includes(token))
  if (seniorMatch && (remoteMatch || dfwMatch) && !weakSignals) return 'strong'
  if (seniorMatch || remoteMatch || dfwMatch) return 'maybe'
  return 'weak'
}

function duplicateRiskFor(company: string, role: string): StagedOpportunity['duplicateRisk'] {
  const text = `${company} ${role}`.toLowerCase()
  if (['senior product designer', 'principal product designer'].some((token) => text.includes(token))) return 'medium'
  if (text.includes('design system') || text.includes('mobile')) return 'high'
  return 'low'
}

function parseBoard(value: string) {
  const match = value.match(/direct board scan \(([^)]+)\)/i)
  return match?.[1] ?? 'direct_board'
}

function parseBoardJobId(value: string) {
  const match = value.match(/job_board_id:([^|\s]+)/i)
  return match?.[1]
}

function reasonsFor(role: string, location: string, notes: string): string[] {
  const reasons: string[] = []
  const roleText = role.toLowerCase()
  const locationText = location.toLowerCase()
  if (['principal', 'lead', 'staff', 'senior'].some((token) => roleText.includes(token))) reasons.push('target seniority')
  if (locationText.includes('remote')) reasons.push('remote allowed')
  if (['dallas', 'fort worth', 'dfw', 'plano', 'irving', 'frisco'].some((token) => locationText.includes(token))) reasons.push('DFW-compatible')
  if (notes.toLowerCase().includes('builtin')) reasons.push('board provenance captured')
  return reasons.length ? reasons : ['needs manual fit review']
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

export function adaptDirectBoardPreview(previewRows: string[][]): StagedOpportunity[] {
  return previewRows.map((row) => {
    const [jobId, company, role, location, , , , nextStep, , directLink, postingLink, , source, notes] = row
    const fitBand = fitBandFor(role || '', location || '')
    return {
      id: `staged_${jobId}`,
      canonicalJobId: jobId,
      company: company || 'Unknown company',
      role: role || 'Unknown role',
      location: location || 'Unknown location',
      source: source || 'direct_board',
      sourceBoard: parseBoard(notes || source || ''),
      boardJobId: parseBoardJobId(notes || ''),
      provenance: notes || 'Imported from direct board scan',
      status: 'pending',
      trustLevel: 'staged',
      fitBand,
      duplicateRisk: duplicateRiskFor(company || '', role || ''),
      recommendedAction: fitBand === 'strong' ? 'Promote after duplicate check' : fitBand === 'maybe' ? 'Hold for ranked review' : 'Reject unless strategic exception',
      reasons: reasonsFor(role || '', location || '', notes || ''),
      link: directLink || postingLink,
      notes: nextStep || '',
    }
  })
}
