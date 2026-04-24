import actionsMirror from '../../data_mirror/Actions.json'
import jobsMirror from '../../data_mirror/Jobs.json'
import recruitersMirror from '../../data_mirror/Recruiters.json'
import signalsMirror from '../../data_mirror/Signals.json'
import taskRunsMirror from '../../data_mirror/TaskRuns.json'
import latestRunReport from '../../runtime/reports/jt7_run_2026-04-23T21-01-06.235513-05-00.json'

type MirrorRow = Record<string, string>

export type ActionState = 'open' | 'waiting' | 'done' | 'blocked'

export type ExecutionCardItem = {
  id: string
  priority: number
  actionType: string
  status: 'critical' | 'high' | 'medium' | 'low'
  urgency: 'now' | 'soon' | 'later'
  actionState: ActionState
  title: string
  targetLabel: string
  companyName?: string
  jobTitle?: string
  recruiterName?: string
  signalIds: string[]
  primarySignalId: string
  whyNow: string
  confidence: number
  reviewRequired: boolean
  primaryCta: string
  secondaryActions: string[]
  dueAt?: string
  createdAt: string
  updatedAt: string
  evidenceSummary: string
  completed?: boolean
}

export type RecentSignalItem = {
  id: string
  signalType: string
  company: string
  timestamp: string
  actionId?: string
}

export type TaskRunSummary = {
  taskRunId: string
  status: string
  lastRunAt: string
  nextRunAt: string
  resultSummary: string
  outputsRef: string
}

export type TodayPlanSummary = {
  completedCount: number
  totalCount: number
  nextBestActionTitle: string
  lastRunTimestamp: string
  operatorSummary: string
}


function rowsToObjects(rows: string[][]): MirrorRow[] {
  const [header, ...data] = rows
  return data.map((row) => {
    const padded = [...row]
    while (padded.length < header.length) padded.push('')
    return Object.fromEntries(header.map((key, index) => [key, padded[index] ?? '']))
  })
}

const jobs = rowsToObjects(jobsMirror)
const recruiters = rowsToObjects(recruitersMirror)
const signals = rowsToObjects(signalsMirror)
const actions = rowsToObjects(actionsMirror)
const taskRuns = rowsToObjects(taskRunsMirror)

function latestTaskRunRow(): MirrorRow | undefined {
  return [...taskRuns].sort((a, b) => Date.parse(b.last_run_at) - Date.parse(a.last_run_at))[0]
}

function recruiterNameFor(job: MirrorRow): string | undefined {
  const recruiter = recruiters.find((row) => row.recruiter_id === job.contact)
  return recruiter?.contact_name || recruiter?.company_name || undefined
}

function validSignals(): MirrorRow[] {
  return signals.filter((signal) => signal.signal_id)
}

function linkedSignalsForJob(jobId: string): MirrorRow[] {
  return validSignals().filter((signal) => signal.linked_job_id === jobId)
}

function confidenceForSignal(signal: MirrorRow): number {
  if (signal.status === 'accepted') return 0.85
  if (signal.status === 'review_required_no_job_create') return 0.5
  if (signal.status === 'review_needed') return 0.5
  return 0.35
}

function priorityMeta(signal: MirrorRow, job?: MirrorRow, dueAt?: string) {
  const signalType = signal.signal_type
  const nextStep = job?.next_step ?? ''
  const now = Date.now()
  const detectedAt = signal.detected_at ? Date.parse(signal.detected_at) : NaN
  const dueSoon = dueAt ? Date.parse(dueAt) - now <= 1000 * 60 * 60 * 48 : false
  const recruiterRecent = !Number.isNaN(detectedAt) && now - detectedAt <= 1000 * 60 * 60 * 24
  const followUpWindow = !Number.isNaN(detectedAt) && now - detectedAt <= 1000 * 60 * 60 * 24 * 5

  if (signalType === 'interview_scheduling' || signalType === 'reschedule') {
    return { priority: 1, status: 'critical' as const, urgency: 'now' as const }
  }
  if ((signalType === 'reply_received' || signalType === 'recruiter_outreach') && recruiterRecent) {
    return { priority: 1, status: 'critical' as const, urgency: 'now' as const }
  }
  if (dueSoon) {
    return { priority: 1, status: 'critical' as const, urgency: 'now' as const }
  }
  if (signal.status === 'review_required_no_job_create') {
    return { priority: 2, status: 'high' as const, urgency: 'soon' as const }
  }
  if (signalType === 'follow_up_opportunity' && followUpWindow) {
    return { priority: 3, status: 'medium' as const, urgency: 'soon' as const }
  }
  if (nextStep && confidenceForSignal(signal) >= 0.8) {
    return { priority: 3, status: 'medium' as const, urgency: 'soon' as const }
  }
  return { priority: 5, status: 'low' as const, urgency: 'later' as const }
}

function actionStateForCard(card: {
  reviewRequired: boolean
  dueAt?: string
  whyNow: string
}): ActionState {
  if (card.reviewRequired) return 'blocked'
  if (card.whyNow.toLowerCase().includes('waiting')) return 'waiting'
  return 'open'
}

function buildSignalDrivenCards(): ExecutionCardItem[] {
  const cards: ExecutionCardItem[] = []
  const added = new Set<string>()

  for (const signal of validSignals()) {
    const job = signal.linked_job_id ? jobs.find((item) => item.job_id === signal.linked_job_id) : undefined
    const hasValidJob = Boolean(job && signal.linked_job_id)
    const reviewRequired = signal.status === 'review_required_no_job_create' || signal.status === 'review_needed'

    if (!hasValidJob && !reviewRequired) continue
    if (!reviewRequired && confidenceForSignal(signal) < 0.8) continue

    const dueAt = signal.signal_type === 'follow_up_opportunity' ? '2026-04-24T09:00:00-05:00' : undefined
    const { priority, status, urgency } = priorityMeta(signal, job, dueAt)
    const cardId = `card_${signal.signal_id}`
    if (added.has(cardId)) continue
    added.add(cardId)

    const companyName = signal.company || job?.company || ''
    const jobTitle = signal.role || job?.role || ''
    const recruiterName = job ? recruiterNameFor(job) : undefined
    const whyNow = reviewRequired
      ? 'This signal was preserved but blocked from job creation. It needs an operator review before tracker mutation.'
      : job?.next_step
        ? `JT7 has a live next step for this job: ${job.next_step}.`
        : 'This signal is linked to a real job and is ready for the next operator move.'

    const evidenceSummary = signal.raw_excerpt || `${signal.signal_type} detected for ${companyName}`
    const title = reviewRequired
      ? `Review ${companyName || 'unmapped'} signal before job creation`
      : signal.signal_type === 'follow_up_opportunity'
        ? `Respond to ${companyName} follow-up`
        : job?.next_step || `Review ${companyName} opportunity`

    cards.push({
      id: cardId,
      priority,
      actionType: reviewRequired ? 'review_required' : signal.signal_type,
      status,
      title,
      targetLabel: recruiterName || companyName || 'JT7',
      companyName: companyName || undefined,
      jobTitle: jobTitle || undefined,
      recruiterName,
      signalIds: [signal.signal_id],
      primarySignalId: signal.signal_id,
      whyNow,
      confidence: confidenceForSignal(signal),
      reviewRequired,
      urgency,
      actionState: actionStateForCard({ reviewRequired, dueAt, whyNow }),
      primaryCta: reviewRequired ? 'Review signal' : 'Open job',
      secondaryActions: reviewRequired ? ['Ignore', 'Defer'] : ['Mark waiting', 'Defer'],
      dueAt,
      createdAt: signal.detected_at || latestRunReport.runTimestamp || '',
      updatedAt: latestRunReport.runTimestamp || signal.detected_at || '',
      evidenceSummary,
      completed: false,
    })
  }

  return cards
}

function buildActionBackedCards(): ExecutionCardItem[] {
  return actions
    .filter((action) => action.status === 'open')
    .map((action) => {
      const job = jobs.find((item) => item.job_id === action.job_id)
      const linkedSignals = linkedSignalsForJob(action.job_id)
      const primarySignal = linkedSignals[0]
      if (!job || !primarySignal) return null

      const { priority, status, urgency } = priorityMeta(primarySignal, job, action.due_at || undefined)
      return {
        id: `action_${action.action_id}`,
        priority,
        actionType: action.instruction.toLowerCase().replaceAll(' ', '_'),
        status,
        title: action.instruction,
        targetLabel: action.company || job.company,
        companyName: job.company,
        jobTitle: job.role,
        recruiterName: recruiterNameFor(job),
        signalIds: linkedSignals.map((signal) => signal.signal_id),
        primarySignalId: primarySignal.signal_id,
        whyNow: action.reason || `Open action for ${job.company}`,
        confidence: confidenceForSignal(primarySignal),
        reviewRequired: false,
        urgency,
        actionState: action.status === 'done' ? 'done' : action.status === 'blocked' ? 'blocked' : action.status === 'waiting' ? 'waiting' : 'open',
        primaryCta: 'Open action',
        secondaryActions: ['Mark done', 'Defer'],
        dueAt: action.due_at || undefined,
        createdAt: action.created_at,
        updatedAt: latestRunReport.runTimestamp || action.created_at,
        evidenceSummary: primarySignal.raw_excerpt,
        completed: false,
      } satisfies ExecutionCardItem
    })
    .filter(Boolean) as ExecutionCardItem[]
}

function dedupeKey(card: ExecutionCardItem) {
  return [
    card.primarySignalId,
    card.companyName ?? '',
    card.recruiterName ?? '',
    card.actionType,
    card.targetLabel,
  ].join('|')
}

function uniqueCards(cards: ExecutionCardItem[]): ExecutionCardItem[] {
  const seen = new Set<string>()
  return cards.filter((card) => {
    const key = dedupeKey(card)
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
}

function byExecutionOrder(a: ExecutionCardItem, b: ExecutionCardItem) {
  if (a.priority !== b.priority) return a.priority - b.priority
  const aDue = a.dueAt ? Date.parse(a.dueAt) : Number.MAX_SAFE_INTEGER
  const bDue = b.dueAt ? Date.parse(b.dueAt) : Number.MAX_SAFE_INTEGER
  if (aDue !== bDue) return aDue - bDue
  return Date.parse(a.createdAt) - Date.parse(b.createdAt)
}

function isInterviewRelated(card: ExecutionCardItem) {
  return card.actionType.includes('interview') || card.actionType === 'reschedule'
}

function isRecruiterReply(card: ExecutionCardItem) {
  return card.actionType.includes('reply_received') || card.actionType.includes('recruiter_outreach') || card.actionType.includes('respond_to_outreach')
}

function blocksPipelineProgression(card: ExecutionCardItem) {
  return card.reviewRequired && (card.evidenceSummary.toLowerCase().includes('blocked') || card.whyNow.toLowerCase().includes('before tracker mutation'))
}

function highConfidenceCompany(card: ExecutionCardItem) {
  return card.confidence >= 0.8 && Boolean(card.companyName)
}

function includeInTodayPlan(card: ExecutionCardItem) {
  if (card.priority === 1 || card.status === 'critical') return true
  if (card.dueAt && Date.parse(card.dueAt) - Date.now() <= 1000 * 60 * 60 * 48) return true
  if (isInterviewRelated(card)) return true
  if (isRecruiterReply(card)) return true
  if (card.reviewRequired && (blocksPipelineProgression(card) || highConfidenceCompany(card))) return true
  return false
}

function rankedBacklog(): ExecutionCardItem[] {
  return uniqueCards([...buildActionBackedCards(), ...buildSignalDrivenCards()])
    .filter((item) => !item.completed)
    .filter((item) => includeInTodayPlan(item))
    .sort(byExecutionOrder)
}

export function getNextBestAction(): ExecutionCardItem | null {
  const backlog = rankedBacklog()
  const next = backlog[0]
  if (next) {
    return { ...next, urgency: 'now' }
  }
  const fallback = uniqueCards([...buildActionBackedCards(), ...buildSignalDrivenCards()])
    .filter((item) => !item.completed)
    .sort(byExecutionOrder)[0]
  return fallback ? { ...fallback, urgency: 'now' } : null
}

export function getExecutionCards(): ExecutionCardItem[] {
  const next = getNextBestAction()
  const rest = rankedBacklog()
    .filter((item) => item.id !== next?.id)
    .filter((item) => item.actionState === 'open' || item.actionState === 'blocked')
  return rest.slice(0, 8)
}

export function getCompletedToday(): ExecutionCardItem[] {
  return uniqueCards([...buildActionBackedCards(), ...buildSignalDrivenCards()]).filter((item) => item.actionState === 'done')
}

export function getWaitingActions(): ExecutionCardItem[] {
  return uniqueCards([...buildActionBackedCards(), ...buildSignalDrivenCards()]).filter((item) => item.actionState === 'waiting')
}

export function getRecentSignals(): RecentSignalItem[] {
  const visibleCards = [getNextBestAction(), ...getExecutionCards()].filter(Boolean) as ExecutionCardItem[]
  const executionSignalIds = new Set(visibleCards.flatMap((item) => item.signalIds))
  return validSignals()
    .filter((signal) => executionSignalIds.has(signal.signal_id))
    .map((signal) => ({
      id: signal.signal_id,
      signalType: signal.signal_type,
      company: signal.company || 'Unknown company',
      timestamp: signal.detected_at,
      actionId: getExecutionCards().find((item) => item.signalIds.includes(signal.signal_id))?.id,
    }))
}

export function getLatestTaskRun(): TaskRunSummary | null {
  const latest = latestTaskRunRow()
  if (!latest) return null
  return {
    taskRunId: latest.task_run_id,
    status: latest.status,
    lastRunAt: latest.last_run_at,
    nextRunAt: latest.next_run_at,
    resultSummary: latest.result_summary,
    outputsRef: latest.outputs_ref,
  }
}

export function getTodayPlanSummary(): TodayPlanSummary {
  const cards = getExecutionCards()
  const completed = getCompletedToday()
  const next = getNextBestAction()
  const latest = getLatestTaskRun()

  const backlog = rankedBacklog()
  const nowCount = [next, ...cards].filter((item): item is ExecutionCardItem => Boolean(item)).filter((item) => item.urgency === 'now').length
  const soonCount = [next, ...cards].filter((item): item is ExecutionCardItem => Boolean(item)).filter((item) => item.urgency === 'soon').length
  const shownCount = (next ? 1 : 0) + cards.length
  const backlogCount = Math.max(backlog.length - shownCount, 0)

  return {
    completedCount: completed.length,
    totalCount: cards.length + completed.length,
    nextBestActionTitle: next?.title ?? 'No next action ready',
    lastRunTimestamp: latest?.lastRunAt ?? latestRunReport.runTimestamp ?? 'Unknown',
    operatorSummary: `${shownCount} actions · ${nowCount} now · ${soonCount} soon${backlogCount > 0 ? ` · +${backlogCount} backlog` : ''}`,
  }
}
