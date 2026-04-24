import type { CSSProperties } from 'react'
import type { TodayPlanSummary } from '../../data/selectors'

type ProgressStripProps = {
  summary: TodayPlanSummary
}

export function ProgressStrip({ summary }: ProgressStripProps) {
  return (
    <section style={styles.wrap}>
      <p style={styles.label}>Today’s Plan</p>
      <h1 style={styles.title}>Start with this</h1>
      <p style={styles.metaValue}>{summary.totalCount} things to work through</p>
    </section>
  )
}

const styles: Record<string, CSSProperties> = {
  wrap: {
    border: '1px solid #1e293b',
    backgroundColor: '#111827',
    borderRadius: '0.75rem',
    padding: '1rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  label: {
    margin: 0,
    color: '#93c5fd',
    textTransform: 'uppercase',
    fontSize: '0.75rem',
    letterSpacing: '0.05em',
  },
  title: {
    margin: '0.25rem 0 0',
    fontSize: '1.75rem',
    color: '#f8fafc',
  },
  metaBlock: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.2rem',
  },
  metaLabel: {
    margin: 0,
    color: '#94a3b8',
    fontSize: '0.8rem',
  },
  metaValue: {
    margin: 0,
    color: '#e2e8f0',
  },
}
