export type ExecutionCardItem = {
  id: string
  priority: number
  actionType: string
  title: string
  targetLabel: string
  whyNow: string
  primaryCta: string
  secondaryActions: string[]
  dueAt?: string
  createdAt: string
  completed?: boolean
  signalId?: string
}

export type RecentSignalItem = {
  id: string
  signalType: string
  company: string
  timestamp: string
  actionId?: string
}

export type TodayPlanSummary = {
  completedCount: number
  totalCount: number
  nextBestActionTitle: string
  lastRunTimestamp: string
}

const executionCards: ExecutionCardItem[] = [
  {
    id: 'exec_001',
    priority: 1,
    actionType: 'follow_up',
    title: 'Reply to Thomson Reuters follow-up',
    targetLabel: 'Thomson Reuters',
    whyNow: 'A live follow-up signal is already linked to an active job and should be answered while the thread is warm.',
    primaryCta: 'Open thread',
    secondaryActions: ['Mark waiting', 'Defer'],
    dueAt: '2026-04-24T09:00:00-05:00',
    createdAt: '2026-04-23T20:52:00-05:00',
    signalId: 'signal_017',
  },
  {
    id: 'exec_002',
    priority: 2,
    actionType: 'review',
    title: 'Review medium-confidence LinkedIn alert signals',
    targetLabel: 'ReviewQueue',
    whyNow: 'These signals were intentionally blocked from job creation and need operator judgment before they can affect the tracker.',
    primaryCta: 'Review signals',
    secondaryActions: ['Ignore', 'Defer'],
    dueAt: '2026-04-24T11:00:00-05:00',
    createdAt: '2026-04-23T21:01:06-05:00',
    signalId: 'signal_041',
  },
  {
    id: 'exec_003',
    priority: 3,
    actionType: 'application_review',
    title: 'Review OpenLoop opportunity for fit and response path',
    targetLabel: 'OpenLoop',
    whyNow: 'A strong job alert signal is already linked, so this is ready for an apply-or-ignore decision.',
    primaryCta: 'Review job',
    secondaryActions: ['Archive', 'Later'],
    dueAt: '2026-04-24T13:00:00-05:00',
    createdAt: '2026-04-23T20:52:00-05:00',
    signalId: 'signal_053',
  },
  {
    id: 'exec_004',
    priority: 4,
    actionType: 'cleanup',
    title: 'Clean low-quality signal classifications from today',
    targetLabel: 'Signals',
    whyNow: 'The runtime is preserving review-required signals, but the operator still needs a quick cleanup pass to keep the queue useful.',
    primaryCta: 'Inspect signals',
    secondaryActions: ['Skip today'],
    createdAt: '2026-04-23T21:01:06-05:00',
    completed: true,
    signalId: 'signal_040',
  },
]

const recentSignals: RecentSignalItem[] = [
  {
    id: 'signal_017',
    signalType: 'follow_up_opportunity',
    company: 'Thomson Reuters',
    timestamp: '2026-04-23T20:52:00-05:00',
    actionId: 'exec_001',
  },
  {
    id: 'signal_041',
    signalType: 'job_alert',
    company: '95 Percent Group',
    timestamp: '2026-04-23T21:01:06-05:00',
    actionId: 'exec_002',
  },
  {
    id: 'signal_053',
    signalType: 'job_alert',
    company: 'OpenLoop',
    timestamp: '2026-04-23T20:52:00-05:00',
    actionId: 'exec_003',
  },
]

function byExecutionOrder(a: ExecutionCardItem, b: ExecutionCardItem) {
  if (a.priority !== b.priority) return a.priority - b.priority
  const aDue = a.dueAt ? Date.parse(a.dueAt) : Number.MAX_SAFE_INTEGER
  const bDue = b.dueAt ? Date.parse(b.dueAt) : Number.MAX_SAFE_INTEGER
  if (aDue !== bDue) return aDue - bDue
  return Date.parse(a.createdAt) - Date.parse(b.createdAt)
}

export function getExecutionCards(): ExecutionCardItem[] {
  return executionCards.filter((item) => !item.completed).sort(byExecutionOrder)
}

export function getNextBestAction(): ExecutionCardItem | null {
  return getExecutionCards()[0] ?? null
}

export function getCompletedToday(): ExecutionCardItem[] {
  return executionCards.filter((item) => item.completed)
}

export function getRecentSignals(): RecentSignalItem[] {
  const actionableIds = new Set(executionCards.map((item) => item.signalId).filter(Boolean))
  return recentSignals.filter((signal) => actionableIds.has(signal.id))
}

export function getTodayPlanSummary(): TodayPlanSummary {
  const all = executionCards
  const completed = all.filter((item) => item.completed)
  const next = getNextBestAction()

  return {
    completedCount: completed.length,
    totalCount: all.length,
    nextBestActionTitle: next?.title ?? 'No next action ready',
    lastRunTimestamp: '2026-04-23T21:01:06-05:00',
  }
}
