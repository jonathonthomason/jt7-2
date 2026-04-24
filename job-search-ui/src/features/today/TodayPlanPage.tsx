import type { CSSProperties } from 'react'
import {
  getCompletedToday,
  getExecutionCards,
  getNextBestAction,
  getRecentSignals,
  getTodayPlanSummary,
} from '../../data/selectors'
import { CompletedToday } from './CompletedToday'
import { ExecutionCard } from './ExecutionCard'
import { NextBestAction } from './NextBestAction'
import { ProgressStrip } from './ProgressStrip'
import { SignalNotes } from './SignalNotes'

export function TodayPlanPage() {
  const summary = getTodayPlanSummary()
  const nextBestAction = getNextBestAction()
  const executionCards = getExecutionCards().slice(0, 5)
  const completedToday = getCompletedToday()
  const recentSignals = getRecentSignals()

  return (
    <section style={styles.page}>
      <ProgressStrip summary={summary} />
      <NextBestAction item={nextBestAction} />
      <section style={styles.section}>
        <div style={styles.list}>
          {executionCards.map((item) => (
            <ExecutionCard key={item.id} {...item} emphasis="secondary" />
          ))}
        </div>
      </section>
      <CompletedToday items={completedToday} />
      {recentSignals.length > 0 ? <SignalNotes items={recentSignals} /> : null}
    </section>
  )
}

const styles: Record<string, CSSProperties> = {
  page: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.25rem',
  },
  section: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.9rem',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.95rem',
  },
}
