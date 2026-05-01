import { createContext, useContext, useMemo, useState, type ReactNode } from 'react'
import actionsMirror from '../../data_mirror/Actions.json'
import competitionMirror from '../../data_mirror/Competition.json'
import jobsMirror from '../../data_mirror/Jobs.json'
import recruitersMirror from '../../data_mirror/Recruiters.json'
import reviewQueueMirror from '../../data_mirror/ReviewQueue.json'
import signalsMirror from '../../data_mirror/Signals.json'
import taskRunsMirror from '../../data_mirror/TaskRuns.json'
import directBoardImportPreview from '../../runtime/direct_board_import_preview.json'
import { buildFallbackReviewSelection } from '../domain/cockpit/fixtures'
import { rowsToObjects, adaptDirectBoardPreview, adaptReviewQueue } from '../domain/cockpit/mirrorAdapters'
import { confirmAsNewOpportunity, deferSignal, dismissSignal, escalateSignal, linkToExistingOpportunity, markDuplicate } from '../domain/cockpit/reviewActions'
import type { ReviewCommand } from '../domain/cockpit/enums'
import type { ReviewEvent, ReviewItem, StagedOpportunity } from '../domain/cockpit/types'

const STORAGE_KEY = 'jt7_mvp_state_v1_5'

type MirrorRow = Record<string, string>
type PanelType = 'signal' | 'job' | 'recruiter' | 'action' | 'message' | 'review' | 'staging' | null

export type MvpSignal = {
  id: string
  type: string
  source: string
  timestamp: string
  priority: 'critical' | 'high' | 'medium' | 'low'
  company: string
  role: string
  recruiter?: string
  summary: string
  whyItMatters: string
  status: 'new' | 'reviewing' | 'linked' | 'dismissed' | 'complete'
  linkedJobId?: string
}

export type MvpJob = {
  id: string
  role: string
  company: string
  status: 'Found' | 'Saved' | 'Reviewing' | 'Applied' | 'Interviewing' | 'Offer' | 'Rejected' | 'Archived' | 'Cold' | 'Recruiter Contacted'
  source: string
  priority: 'critical' | 'high' | 'medium' | 'low'
  dateFound: string
  dateApplied?: string
  lastSignal?: string
  nextAction: string
  recruiterId?: string
  recruiterName?: string
  link?: string
  notes?: string
}

export type MvpRecruiter = {
  id: string
  name: string
  company: string
  status: 'New' | 'Active' | 'Warm' | 'Waiting' | 'Follow-up Due' | 'Inactive' | 'Do Not Contact'
  lastContact?: string
  nextAction: string
  relatedJobs: string[]
  notes?: string
  email?: string
}

export type MvpAction = {
  id: string
  jobId?: string
  company: string
  title: string
  channel: string
  target: string
  whyNow: string
  priority: number
  status: 'open' | 'waiting' | 'done' | 'blocked' | 'deferred' | 'dismissed'
  actionType: string
  primaryCta: string
  secondaryActions: string[]
  createdAt: string
  completedAt?: string
  note?: string
}

export type MvpMessage = {
  id: string
  direction: 'inbound' | 'outbound' | 'draft'
  contact: string
  company: string
  subject: string
  status: string
  relatedJob?: string
  recommendedAction: string
  timestamp: string
}

export type MvpOutreach = {
  id: string
  contact: string
  company: string
  channel: string
  messageType: string
  status: string
  sentDate?: string
  followUpDate?: string
  relatedJob?: string
}

export type MvpTaskRun = {
  id: string
  type: string
  status: string
  lastRunAt: string
  nextRunAt?: string
  summary: string
  outputsRef?: string
}

export type MvpState = {
  signals: MvpSignal[]
  jobs: MvpJob[]
  recruiters: MvpRecruiter[]
  actions: MvpAction[]
  outreach: MvpOutreach[]
  messages: MvpMessage[]
  taskRuns: MvpTaskRun[]
  reviewQueue: ReviewItem[]
  reviewEvents: ReviewEvent[]
  stagingQueue: StagedOpportunity[]
  competition: MirrorRow[]
  selectedPanel: { type: PanelType; id?: string }
  lastUpdated: string
}

type MvpContextValue = {
  state: MvpState
  today: {
    nextAction: MvpAction | null
    openActions: MvpAction[]
    newSignals: MvpSignal[]
    waitingActions: MvpAction[]
    completedToday: MvpAction[]
    completedCount: number
    totalCount: number
    latestRun: MvpTaskRun | null
  }
  reviewSummary: {
    pending: ReviewItem[]
    resolved: ReviewItem[]
    highPriority: ReviewItem[]
  }
  stagingSummary: {
    pending: StagedOpportunity[]
    strongFit: StagedOpportunity[]
    reviewed: StagedOpportunity[]
  }
  runSweep: () => void
  refreshPlan: () => void
  openPanel: (type: Exclude<PanelType, null>, id: string) => void
  closePanel: () => void
  actionCommand: (actionId: string, command: string, note?: string) => void
  signalCommand: (signalId: string, command: string) => void
  reviewCommand: (reviewId: string, command: ReviewCommand, notes?: string) => void
  stagingCommand: (stagingId: string, command: 'Promote' | 'Merge' | 'Hold' | 'Reject', notes?: string) => void
  jobCommand: (jobId: string, command: string, value?: string) => void
  recruiterCommand: (recruiterId: string, command: string, note?: string) => void
  updatePanelNote: (text: string) => void
}

const jobsRows = rowsToObjects(jobsMirror as string[][])
const recruiterRows = rowsToObjects(recruitersMirror as string[][])
const signalRows = rowsToObjects(signalsMirror as string[][])
const actionRows = rowsToObjects(actionsMirror as string[][])
const taskRunRows = rowsToObjects(taskRunsMirror as string[][])

function priorityFrom(value: string): MvpJob['priority'] {
  const lower = value.toLowerCase()
  if (lower.includes('critical') || lower.includes('interview')) return 'critical'
  if (lower.includes('high') || lower.includes('reply')) return 'high'
  if (lower.includes('medium')) return 'medium'
  return 'low'
}

function jobStatus(status: string): MvpJob['status'] {
  const lower = status.toLowerCase()
  if (lower.includes('interview')) return 'Interviewing'
  if (lower.includes('applied')) return 'Applied'
  if (lower.includes('offer')) return 'Offer'
  if (lower.includes('reject')) return 'Rejected'
  if (lower.includes('archive')) return 'Archived'
  if (lower.includes('review')) return 'Reviewing'
  if (lower.includes('save')) return 'Saved'
  if (lower.includes('recruiter')) return 'Recruiter Contacted'
  if (lower.includes('cold') || lower.includes('not applied')) return 'Cold'
  return 'Found'
}

function recruiterStatus(status: string): MvpRecruiter['status'] {
  const lower = status.toLowerCase()
  if (lower.includes('waiting')) return 'Waiting'
  if (lower.includes('follow')) return 'Follow-up Due'
  if (lower.includes('active')) return 'Active'
  if (lower.includes('warm')) return 'Warm'
  if (lower.includes('inactive')) return 'Inactive'
  if (lower.includes('do not')) return 'Do Not Contact'
  return 'New'
}

function actionStatus(status: string): MvpAction['status'] {
  if (status === 'done') return 'done'
  if (status === 'waiting') return 'waiting'
  if (status === 'blocked') return 'blocked'
  if (status === 'deferred') return 'deferred'
  if (status === 'dismissed') return 'dismissed'
  return 'open'
}

function actionTypeFrom(instruction: string) {
  const text = instruction.toLowerCase()
  if (text.includes('reply')) return 'reply'
  if (text.includes('apply')) return 'apply'
  if (text.includes('follow')) return 'follow_up'
  if (text.includes('review')) return 'review_job'
  return 'operator_action'
}

function primaryCtaFor(type: string) {
  if (type === 'reply') return 'Draft Reply'
  if (type === 'apply') return 'Apply'
  if (type === 'follow_up') return 'Follow Up'
  if (type === 'review_job') return 'Review Job'
  return 'Open Detail'
}

function normalizeText(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()
}

function locationAllowed(location: string) {
  const text = normalizeText(location)
  return text.includes('remote') || ['dallas', 'fort worth', 'dfw', 'irving', 'plano', 'frisco', 'addison', 'grapevine', 'arlington', 'richardson'].some((token) => text.includes(token))
}

function roleTier(role: string) {
  const text = normalizeText(role)
  if (['principal product designer', 'lead product designer', 'staff product designer', 'product design manager'].some((token) => text.includes(token))) return 3
  if (text.includes('senior product designer')) return 2
  if (text.includes('product designer') || text.includes('design lead') || text.includes('founding product designer')) return 1
  return 0
}

function weakRolePenalty(role: string) {
  const text = normalizeText(role)
  let penalty = 0
  if (['design system', 'mobile', 'visual', 'brand', 'ui designer'].some((token) => text.includes(token))) penalty += 2
  if (['ux ui', 'production', 'marketing designer'].some((token) => text.includes(token))) penalty += 2
  return penalty
}

function duplicateMatchesFor(staged: StagedOpportunity, jobs: MvpJob[]) {
  const stagedCompany = normalizeText(staged.company)
  const stagedRole = normalizeText(staged.role)
  return jobs.filter((job) => {
    const jobCompany = normalizeText(job.company)
    const jobRole = normalizeText(job.role)
    const sameCompany = stagedCompany && jobCompany === stagedCompany
    const exactRole = stagedRole && jobRole === stagedRole
    const nearRole = stagedRole && jobRole && (jobRole.includes(stagedRole) || stagedRole.includes(jobRole))
    return sameCompany && (exactRole || nearRole)
  }).map((job) => job.id)
}

function scoreStagedOpportunity(staged: StagedOpportunity, jobs: MvpJob[]) {
  let score = 0
  const duplicateMatches = duplicateMatchesFor(staged, jobs)
  const tier = roleTier(staged.role)
  const allowedLocation = locationAllowed(staged.location)
  score += tier * 25
  if (allowedLocation) score += 20
  if (normalizeText(staged.location).includes('remote')) score += 10
  score -= weakRolePenalty(staged.role) * 10
  score -= duplicateMatches.length > 0 ? 35 : 0
  score += staged.sourceBoard === 'builtin' ? 5 : 0
  const fitBand: StagedOpportunity['fitBand'] = score >= 55 ? 'strong' : score >= 25 ? 'maybe' : 'weak'
  const duplicateRisk: StagedOpportunity['duplicateRisk'] = duplicateMatches.length > 1 ? 'high' : duplicateMatches.length === 1 ? 'medium' : staged.duplicateRisk
  const reasons = [...staged.reasons]
  if (duplicateMatches.length) reasons.unshift(`possible canonical duplicate (${duplicateMatches.length})`)
  if (!allowedLocation) reasons.push('outside preferred location rule')
  if (tier === 0) reasons.push('outside target role set')
  const autoStatus: StagedOpportunity['status'] = staged.status === 'promote' || staged.status === 'reject' ? staged.status : tier === 0 ? 'reject' : !allowedLocation ? 'hold' : staged.status
  const recommendedAction = duplicateMatches.length
    ? 'Merge into canonical job or hold for duplicate review'
    : autoStatus === 'reject'
      ? 'Reject by search requirements unless strategic exception'
      : autoStatus === 'hold'
        ? 'Hold for manual location/fit review'
        : fitBand === 'strong'
          ? 'Promote after final human check'
          : fitBand === 'maybe'
            ? 'Hold for ranked review'
            : 'Reject unless strategic exception'

  return {
    ...staged,
    status: autoStatus,
    fitScore: score,
    fitBand,
    duplicateRisk,
    duplicateMatches,
    reasons,
    recommendedAction,
  }
}

function enrichStagingQueue(stagingQueue: StagedOpportunity[], jobs: MvpJob[]) {
  return stagingQueue
    .map((item) => scoreStagedOpportunity(item, jobs))
    .sort((a, b) => (b.fitScore ?? 0) - (a.fitScore ?? 0))
}

function buildInitialState(): MvpState {
  const recruiters = recruiterRows.map((row) => ({
    id: row.recruiter_id,
    name: row.contact_name || row.company_name || 'Unknown recruiter',
    company: row.company_name || 'Unknown company',
    status: recruiterStatus(row.tracking_status || ''),
    lastContact: '',
    nextAction: row.tracking_status?.toLowerCase().includes('follow') ? 'Follow up' : 'Review relationship',
    relatedJobs: jobsRows.filter((job) => job.contact === row.recruiter_id).map((job) => job.job_id),
    email: row.email,
    notes: row.profile_link || '',
  })) satisfies MvpRecruiter[]

  const jobs = jobsRows.map((row) => {
    const recruiter = recruiters.find((item) => item.id === row.contact)
    return {
      id: row.job_id,
      role: row.role || 'Unknown role',
      company: row.company || 'Unknown company',
      status: jobStatus(row.status || ''),
      source: row.source || 'local mirror',
      priority: priorityFrom(`${row.status} ${row.next_step}`),
      dateFound: row.last_contact_date || '2026-04-22',
      dateApplied: row.status?.toLowerCase().includes('applied') ? row.last_contact_date : undefined,
      lastSignal: signalRows.find((signal) => signal.linked_job_id === row.job_id)?.signal_id,
      nextAction: row.next_step || 'Review job fit',
      recruiterId: recruiter?.id,
      recruiterName: recruiter?.name,
      link: row.direct_application_link || row.job_posting_link,
      notes: row.notes,
    }
  }) satisfies MvpJob[]

  const signals = signalRows.map((row) => ({
    id: row.signal_id,
    type: row.signal_type || 'system_alert',
    source: row.source || 'local mirror',
    timestamp: row.detected_at || new Date().toISOString(),
    priority: priorityFrom(`${row.signal_type} ${row.status}`),
    company: row.company || 'Unknown company',
    role: row.role || '',
    recruiter: undefined,
    summary: row.raw_excerpt || `${row.signal_type} detected`,
    whyItMatters: row.status?.includes('review') ? 'Needs review before tracker mutation.' : 'May update pipeline state or create an action.',
    status: row.status?.includes('accepted') ? 'linked' : row.status?.includes('review') ? 'reviewing' : 'new',
    linkedJobId: row.linked_job_id || undefined,
  })) satisfies MvpSignal[]

  const reviewQueue = buildFallbackReviewSelection(adaptReviewQueue(reviewQueueMirror as string[][], signalRows))
  const stagingQueue = enrichStagingQueue(adaptDirectBoardPreview((directBoardImportPreview.proposed_rows || []) as string[][]), jobs)

  const actions = actionRows.map((row) => {
    const job = jobs.find((item) => item.id === row.job_id)
    const actionType = actionTypeFrom(row.instruction || '')
    return {
      id: row.action_id,
      jobId: row.job_id || undefined,
      company: row.company || job?.company || 'JT7',
      title: row.instruction || 'Review next step',
      channel: actionType === 'reply' || actionType === 'follow_up' ? 'Email' : actionType === 'apply' ? 'Job board' : 'JT7',
      target: job?.recruiterName || row.company || job?.company || 'JT7',
      whyNow: row.reason || 'Generated from existing action tracker.',
      priority: row.urgency === 'high' ? 1 : row.urgency === 'medium' ? 2 : 3,
      status: actionStatus(row.status || ''),
      actionType,
      primaryCta: primaryCtaFor(actionType),
      secondaryActions: ['Mark Waiting', 'Defer', 'Complete'],
      createdAt: row.created_at || new Date().toISOString(),
    }
  }) satisfies MvpAction[]

  const messages = signals.slice(0, 12).map((signal) => ({
    id: `message_${signal.id}`,
    direction: signal.type.includes('outreach') || signal.type.includes('reply') ? 'inbound' : 'draft',
    contact: signal.recruiter || signal.company,
    company: signal.company,
    subject: signal.summary.slice(0, 80),
    status: signal.status,
    relatedJob: signal.linkedJobId,
    recommendedAction: signal.status === 'new' ? 'Review signal' : 'Open related job',
    timestamp: signal.timestamp,
  })) satisfies MvpMessage[]

  const outreach = recruiters.slice(0, 12).map((recruiter) => ({
    id: `outreach_${recruiter.id}`,
    contact: recruiter.name,
    company: recruiter.company,
    channel: 'Email',
    messageType: 'Follow-up',
    status: recruiter.status === 'Waiting' ? 'waiting' : 'draft',
    followUpDate: recruiter.status === 'Follow-up Due' ? new Date().toISOString() : undefined,
    relatedJob: recruiter.relatedJobs[0],
  })) satisfies MvpOutreach[]

  const taskRuns = taskRunRows.map((row) => ({
    id: row.task_run_id,
    type: row.task_type || 'JT7_CHAIN',
    status: row.status || 'complete',
    lastRunAt: row.last_run_at,
    nextRunAt: row.next_run_at,
    summary: row.result_summary || row.outputs_ref || 'Task run completed.',
    outputsRef: row.outputs_ref,
  })) satisfies MvpTaskRun[]

  return {
    signals,
    jobs,
    recruiters,
    actions,
    outreach,
    messages,
    taskRuns,
    reviewQueue,
    reviewEvents: [],
    stagingQueue,
    competition: rowsToObjects(competitionMirror as string[][]),
    selectedPanel: { type: null },
    lastUpdated: taskRuns[0]?.lastRunAt || new Date().toISOString(),
  }
}

function normalizeState(state: MvpState): MvpState {
  return {
    ...state,
    stagingQueue: enrichStagingQueue(state.stagingQueue ?? adaptDirectBoardPreview((directBoardImportPreview.proposed_rows || []) as string[][]), state.jobs),
  }
}

function loadInitialState(): MvpState {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) return normalizeState(JSON.parse(stored) as MvpState)
  } catch {
    // Fall through to seeded state.
  }
  return normalizeState(buildInitialState())
}

function createMockSignal(index: number): MvpSignal {
  const sources = ['Gmail', 'LinkedIn', 'Indeed', 'Otta', 'Workday', 'Greenhouse', 'company career pages']
  const companies = ['Figma', 'Capital One', 'ServiceNow', 'Adobe', 'Miro']
  const company = companies[index % companies.length]
  const source = sources[index % sources.length]
  return {
    id: `signal_mvp_${Date.now()}`,
    type: source === 'Gmail' ? 'RECRUITER_REPLY' : 'JOB_BOARD_OPPORTUNITY',
    source,
    timestamp: new Date().toISOString(),
    priority: index % 3 === 0 ? 'high' : 'medium',
    company,
    role: index % 2 === 0 ? 'Principal Product Designer' : 'Senior Product Designer',
    recruiter: source === 'Gmail' ? `${company} Talent` : undefined,
    summary: `${source} surfaced a relevant ${company} product design opportunity.`,
    whyItMatters: 'Matches senior/principal product design target and should be reviewed for fit.',
    status: 'new',
  }
}

const MvpContext = createContext<MvpContextValue | null>(null)

export function MvpStateProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<MvpState>(() => loadInitialState())

  const persist = (next: MvpState) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
    return next
  }

  const today = useMemo(() => {
    const active = state.actions.filter((action) => action.status === 'open' || action.status === 'blocked').sort((a, b) => a.priority - b.priority)
    const completedToday = state.actions.filter((action) => action.status === 'done')
    return {
      nextAction: active[0] ?? null,
      openActions: active.slice(1, 9),
      newSignals: state.signals.filter((signal) => signal.status === 'new' || signal.status === 'reviewing').slice(0, 8),
      waitingActions: state.actions.filter((action) => action.status === 'waiting' || action.status === 'deferred'),
      completedToday,
      completedCount: completedToday.length,
      totalCount: active.length + completedToday.length,
      latestRun: [...state.taskRuns].sort((a, b) => Date.parse(b.lastRunAt) - Date.parse(a.lastRunAt))[0] ?? null,
    }
  }, [state])

  const reviewSummary = useMemo(() => ({
    pending: state.reviewQueue.filter((item) => item.status === 'pending' || item.status === 'deferred'),
    resolved: state.reviewQueue.filter((item) => !['pending', 'deferred'].includes(item.status)),
    highPriority: state.reviewQueue.filter((item) => item.priority === 'high'),
  }), [state.reviewQueue])

  const stagingSummary = useMemo(() => ({
    pending: state.stagingQueue.filter((item) => item.status === 'pending' || item.status === 'hold'),
    strongFit: state.stagingQueue.filter((item) => item.fitBand === 'strong' && !item.duplicateMatches?.length),
    reviewed: state.stagingQueue.filter((item) => item.status === 'promote' || item.status === 'reject'),
  }), [state.stagingQueue])

  const setPersistedState = (updater: (current: MvpState) => MvpState) => {
    setState((current) => persist(updater(current)))
  }

  const openPanel = (type: Exclude<PanelType, null>, id: string) => setPersistedState((current) => ({ ...current, selectedPanel: { type, id } }))
  const closePanel = () => setPersistedState((current) => ({ ...current, selectedPanel: { type: null } }))

  const actionCommand = (actionId: string, command: string, note?: string) => setPersistedState((current) => {
    const now = new Date().toISOString()
    const statusByCommand: Record<string, MvpAction['status']> = {
      Complete: 'done',
      'Mark Waiting': 'waiting',
      Defer: 'deferred',
      Dismiss: 'dismissed',
      Apply: 'done',
      'Review Job': 'done',
      'Follow Up': 'waiting',
      'Draft Reply': 'waiting',
      Reply: 'waiting',
      Draft: 'waiting',
    }
    return {
      ...current,
      actions: current.actions.map((action) => action.id === actionId
        ? { ...action, status: statusByCommand[command] ?? action.status, completedAt: statusByCommand[command] === 'done' ? now : action.completedAt, note: note ?? action.note }
        : action),
      lastUpdated: now,
    }
  })

  const signalCommand = (signalId: string, command: string) => setPersistedState((current) => {
    const now = new Date().toISOString()
    const signal = current.signals.find((item) => item.id === signalId)
    if (!signal) return current
    const linkedStatus: MvpSignal['status'] = command === 'Dismiss' ? 'dismissed' : command === 'Complete' ? 'complete' : 'linked'
    const newAction: MvpAction | null = command === 'Create Action' ? {
      id: `action_${signal.id}`,
      company: signal.company,
      title: `Review ${signal.company} ${signal.role || 'signal'}`,
      channel: signal.source,
      target: signal.recruiter || signal.company,
      whyNow: signal.whyItMatters,
      priority: signal.priority === 'critical' ? 1 : signal.priority === 'high' ? 2 : 3,
      status: 'open',
      actionType: 'review_job',
      primaryCta: 'Review Job',
      secondaryActions: ['Mark Waiting', 'Defer', 'Complete'],
      createdAt: now,
    } : null
    return {
      ...current,
      signals: current.signals.map((item) => item.id === signalId ? { ...item, status: linkedStatus } : item),
      actions: newAction && !current.actions.some((action) => action.id === newAction.id) ? [newAction, ...current.actions] : current.actions,
      lastUpdated: now,
    }
  })

  const reviewCommand = (reviewId: string, command: ReviewCommand, notes?: string) => setPersistedState((current) => {
    const item = current.reviewQueue.find((entry) => entry.id === reviewId)
    if (!item) return current

    const payload = { notes, linkedJobId: item.proposedJobUpdate.linkedJobId }
    const result = command === 'Confirm'
      ? confirmAsNewOpportunity(item, payload)
      : command === 'Link'
        ? linkToExistingOpportunity(item, payload)
        : command === 'Dismiss'
          ? dismissSignal(item, payload)
          : command === 'Mark Duplicate'
            ? markDuplicate(item, payload)
            : command === 'Defer'
              ? deferSignal(item, payload)
              : escalateSignal(item, payload)

    const now = result.event.timestamp
    const actionFromReview = (command === 'Confirm' || command === 'Link') && item.proposedAction
      ? {
          id: `action_review_${reviewId}`,
          jobId: item.proposedJobUpdate.linkedJobId,
          company: item.extractedCompany || item.proposedJobUpdate.company || 'Unknown company',
          title: item.proposedAction,
          channel: item.source,
          target: item.extractedRecruiter || item.extractedCompany || 'JT7',
          whyNow: item.reasonForReview,
          priority: item.priority === 'high' ? 1 : item.priority === 'medium' ? 2 : 3,
          status: 'open' as const,
          actionType: 'review_follow_up',
          primaryCta: 'Review Job',
          secondaryActions: ['Mark Waiting', 'Defer', 'Complete'],
          createdAt: now,
        }
      : null

    const jobFromReview = command === 'Confirm' && item.extractedCompany
      ? {
          id: item.proposedJobUpdate.linkedJobId || `job_from_${reviewId}`,
          role: item.extractedRole || item.proposedJobUpdate.role || 'Unknown role',
          company: item.extractedCompany || item.proposedJobUpdate.company || 'Unknown company',
          status: jobStatus(item.proposedJobUpdate.proposedStatus || 'Reviewing'),
          source: item.source,
          priority: item.priority,
          dateFound: item.timestamp,
          lastSignal: item.signalId,
          nextAction: item.proposedAction || 'Review opportunity',
          recruiterId: item.extractedRecruiter || undefined,
          recruiterName: current.recruiters.find((r) => r.id === item.extractedRecruiter)?.name,
          notes: item.resolutionNotes || notes,
        }
      : null

    return {
      ...current,
      reviewQueue: current.reviewQueue.map((entry) => entry.id === reviewId ? { ...entry, status: result.nextStatus, resolutionNotes: notes ?? entry.resolutionNotes } : entry),
      reviewEvents: [result.event, ...current.reviewEvents],
      signals: current.signals.map((signal) => signal.id === item.signalId
        ? { ...signal, status: command === 'Dismiss' || command === 'Mark Duplicate' ? 'dismissed' : 'linked', linkedJobId: item.proposedJobUpdate.linkedJobId || signal.linkedJobId }
        : signal),
      jobs: jobFromReview && !current.jobs.some((job) => job.id === jobFromReview.id)
        ? [jobFromReview, ...current.jobs]
        : current.jobs.map((job) => job.id === item.proposedJobUpdate.linkedJobId ? { ...job, status: jobStatus(item.proposedJobUpdate.proposedStatus || job.status), lastSignal: item.signalId } : job),
      actions: actionFromReview && !current.actions.some((action) => action.id === actionFromReview.id) ? [actionFromReview, ...current.actions] : current.actions,
      lastUpdated: now,
    }
  })

  const stagingCommand = (stagingId: string, command: 'Promote' | 'Merge' | 'Hold' | 'Reject', notes?: string) => setPersistedState((current) => {
    const now = new Date().toISOString()
    const target = current.stagingQueue.find((item) => item.id === stagingId)
    if (!target) return current

    const status: StagedOpportunity['status'] = command === 'Promote' || command === 'Merge' ? 'promote' : command === 'Reject' ? 'reject' : 'hold'
    const blockedByDuplicate = command === 'Promote' && (target.duplicateMatches?.length ?? 0) > 0
    const mergeTargetId = command === 'Merge' ? target.duplicateMatches?.[0] : undefined
    const promotedJob: MvpJob | null = command === 'Promote' && !blockedByDuplicate ? {
      id: target.canonicalJobId || `job_${stagingId}`,
      role: target.role,
      company: target.company,
      status: 'Reviewing',
      source: `${target.source}_staged`,
      priority: target.fitBand === 'strong' ? 'high' : target.fitBand === 'maybe' ? 'medium' : 'low',
      dateFound: now,
      nextAction: 'Confirm duplicate check and decide whether to apply',
      link: target.link,
      notes: [target.provenance, notes].filter(Boolean).join(' | '),
    } : null

    const mergedJobs = mergeTargetId
      ? current.jobs.map((job) => job.id === mergeTargetId ? {
          ...job,
          status: job.status === 'Cold' ? 'Reviewing' : job.status,
          nextAction: 'Review fresh staged evidence and confirm canonical state',
          link: job.link || target.link,
          notes: [job.notes, `Merged staged evidence: ${target.provenance}`, notes].filter(Boolean).join(' | '),
        } : job)
      : current.jobs

    const nextJobs = promotedJob && !mergedJobs.some((job) => job.id === promotedJob.id) ? [promotedJob, ...mergedJobs] : mergedJobs
    const nextStaging = current.stagingQueue.map((item) => item.id === stagingId ? { ...item, status: blockedByDuplicate ? 'hold' : status, trustLevel: command === 'Promote' || command === 'Merge' ? 'reviewed' : item.trustLevel, notes: blockedByDuplicate ? [item.notes, 'Promotion blocked by duplicate; merge or hold instead.', notes].filter(Boolean).join(' | ') : notes ?? item.notes } : item)

    return {
      ...current,
      stagingQueue: enrichStagingQueue(nextStaging, nextJobs),
      jobs: nextJobs,
      lastUpdated: now,
    }
  })

  const jobCommand = (jobId: string, command: string, value?: string) => setPersistedState((current) => {
    const now = new Date().toISOString()
    const job = current.jobs.find((item) => item.id === jobId)
    const nextAction: MvpAction | null = command === 'Create Follow-up' && job ? {
      id: `action_followup_${jobId}_${Date.now()}`,
      jobId,
      company: job.company,
      title: `Follow up on ${job.company}`,
      channel: 'Email',
      target: job.recruiterName || job.company,
      whyNow: 'Manual follow-up created from job management.',
      priority: 2,
      status: 'open',
      actionType: 'follow_up',
      primaryCta: 'Follow Up',
      secondaryActions: ['Mark Waiting', 'Defer', 'Complete'],
      createdAt: now,
    } : null
    return {
      ...current,
      jobs: current.jobs.map((item) => item.id === jobId ? {
        ...item,
        status: command === 'Archive' ? 'Archived' : command === 'Update Status' && value ? value as MvpJob['status'] : command === 'Apply' ? 'Applied' : command === 'Review' ? 'Reviewing' : item.status,
        dateApplied: command === 'Apply' ? now : item.dateApplied,
      } : item),
      actions: nextAction ? [nextAction, ...current.actions] : current.actions,
      lastUpdated: now,
    }
  })

  const recruiterCommand = (recruiterId: string, command: string, note?: string) => setPersistedState((current) => {
    const now = new Date().toISOString()
    const recruiter = current.recruiters.find((item) => item.id === recruiterId)
    const newMessage: MvpMessage | null = command === 'Draft Reply' && recruiter ? {
      id: `message_draft_${Date.now()}`,
      direction: 'draft',
      contact: recruiter.name,
      company: recruiter.company,
      subject: `Draft reply to ${recruiter.name}`,
      status: 'draft',
      recommendedAction: 'Review and send manually',
      timestamp: now,
    } : null
    return {
      ...current,
      recruiters: current.recruiters.map((item) => item.id === recruiterId ? {
        ...item,
        status: command === 'Follow Up' ? 'Waiting' : item.status,
        lastContact: command === 'Follow Up' ? now : item.lastContact,
        notes: note ? `${item.notes || ''}\n${note}`.trim() : item.notes,
      } : item),
      messages: newMessage ? [newMessage, ...current.messages] : current.messages,
      lastUpdated: now,
    }
  })

  const updatePanelNote = (text: string) => setPersistedState((current) => {
    const { type, id } = current.selectedPanel
    if (!id) return current
    if (type === 'job') return { ...current, jobs: current.jobs.map((item) => item.id === id ? { ...item, notes: text } : item) }
    if (type === 'recruiter') return { ...current, recruiters: current.recruiters.map((item) => item.id === id ? { ...item, notes: text } : item) }
    if (type === 'action') return { ...current, actions: current.actions.map((item) => item.id === id ? { ...item, note: text } : item) }
    if (type === 'review') return { ...current, reviewQueue: current.reviewQueue.map((item) => item.id === id ? { ...item, resolutionNotes: text } : item) }
    if (type === 'staging') return { ...current, stagingQueue: enrichStagingQueue(current.stagingQueue.map((item) => item.id === id ? { ...item, notes: text } : item), current.jobs) }
    return current
  })

  const runSweep = () => setPersistedState((current) => {
    const now = new Date().toISOString()
    const signal = createMockSignal(current.taskRuns.length)
    const job: MvpJob = {
      id: `job_${signal.id}`,
      role: signal.role,
      company: signal.company,
      status: 'Found',
      source: signal.source,
      priority: signal.priority,
      dateFound: now,
      lastSignal: signal.id,
      nextAction: 'Review job fit',
      recruiterName: signal.recruiter,
    }
    const action: MvpAction = {
      id: `action_${signal.id}`,
      jobId: job.id,
      company: signal.company,
      title: `Review ${signal.company} opportunity`,
      channel: signal.source,
      target: signal.recruiter || signal.company,
      whyNow: signal.whyItMatters,
      priority: signal.priority === 'critical' ? 1 : signal.priority === 'high' ? 2 : 3,
      status: 'open',
      actionType: 'review_job',
      primaryCta: 'Review Job',
      secondaryActions: ['Mark Waiting', 'Defer', 'Complete'],
      createdAt: now,
    }
    const run: MvpTaskRun = {
      id: `taskrun_${Date.now()}`,
      type: 'JT7_CHAIN',
      status: 'complete',
      lastRunAt: now,
      nextRunAt: new Date(Date.now() + 1000 * 60 * 60 * 6).toISOString(),
      summary: 'MVP sweep checked mock adapters, classified one signal, created one job and one action.',
      outputsRef: 'signals:+1|jobs:+1|actions:+1',
    }
    return {
      ...current,
      signals: [signal, ...current.signals],
      jobs: [job, ...current.jobs],
      actions: [action, ...current.actions],
      taskRuns: [run, ...current.taskRuns],
      lastUpdated: now,
    }
  })

  const refreshPlan = () => setPersistedState((current) => ({ ...current, lastUpdated: new Date().toISOString() }))

  return (
    <MvpContext.Provider value={{ state, today, reviewSummary, stagingSummary, runSweep, refreshPlan, openPanel, closePanel, actionCommand, signalCommand, reviewCommand, stagingCommand, jobCommand, recruiterCommand, updatePanelNote }}>
      {children}
    </MvpContext.Provider>
  )
}

export function useMvpState() {
  const value = useContext(MvpContext)
  if (!value) throw new Error('useMvpState must be used within MvpStateProvider')
  return value
}
