export type WritebackCommand = 'Promote' | 'Merge'

type WritebackPlan = {
  action: 'create' | 'merge' | 'hold' | 'reject'
  reason: string
  staged_company: string
  staged_role: string
  matched_job_id?: string
  create_row?: string[] | null
  update_values?: Record<string, string> | null
}

export type StagingWritebackResponse = {
  executedAt: string
  staged: {
    staged_id: string
    preview_index: string
    company: string
    role: string
    location: string
    job_posting_link: string
    source: string
  }
  plan: WritebackPlan
  mode: 'apply' | 'plan'
  result: 'planned' | 'created' | 'merged' | 'hold' | 'reject'
  created_job_id?: string
  merged_job_id?: string
  reportPath: string
}

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8787/api'

export async function applyStagingWriteback(stagedId: string, command: WritebackCommand): Promise<StagingWritebackResponse> {
  const response = await fetch(`${API_BASE}/staging/writeback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stagedId, command, apply: true }),
  })

  const payload = await response.json().catch(() => null)
  if (!response.ok) {
    const message = payload && typeof payload.error === 'string' ? payload.error : `writeback request failed (${response.status})`
    throw new Error(message)
  }

  return payload as StagingWritebackResponse
}
