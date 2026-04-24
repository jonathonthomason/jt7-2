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
  const executionCards = getExecutionCards()
  const completedToday = getCompletedToday()
  const recentSignals = getRecentSignals()

  return (
    <section style={styles.page}>
      <ProgressStrip summary={summary} />
      <NextBestAction item={nextBestAction} />
      <section style={styles.section}>
        <h2 style={styles.heading}>Execution list</h2>
        <div style={styles.list}>
          {executionCards.map((item) => (
            <ExecutionCard key={item.id} {...item} />
          ))}
        </div>
      </section>
      <CompletedToday items={completedToday} />
      <SignalNotes items={recentSignals} />
    </section>
  )
}

const styles: Record<string, CSSProperties> = {
  page: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  section: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  heading: {
    margin: 0,
    color: '#f8fafc',
    fontSize: '1.25rem',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
}
