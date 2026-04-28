import type { CSSProperties } from 'react'
import type { TodayPlanSummary } from '../../data/selectors'

type ProgressStripProps = {
  summary: TodayPlanSummary
}

export function ProgressStrip({ summary }: ProgressStripProps) {
  return (
    <section style={styles.wrap}>
      <div>
        <p style={styles.label}>/execute/today</p>
        <h1 style={styles.title}>Today’s Plan</h1>
      </div>
      <div style={styles.metaBlock}>
        <p style={styles.metaLabel}>Progress</p>
        <strong style={styles.metaValue}>{summary.completedCount}/{summary.totalCount}</strong>
      </div>
      <div style={styles.nextActionBlock}>
        <p style={styles.metaLabel}>Next action</p>
        <p style={styles.nextAction}>{summary.nextBestActionTitle}</p>
      </div>
    </section>
  )
}

const styles: Record<string, CSSProperties> = {
  wrap: {
    border: '1px solid #2a2f3a',
    borderTop: '3px solid #0f62fe',
    backgroundColor: '#161616',
    borderRadius: 0,
    padding: '1rem',
    display: 'flex',
    alignItems: 'end',
    justifyContent: 'space-between',
    gap: '1rem',
    textAlign: 'left',
  },
  label: {
    margin: 0,
    color: '#78a9ff',
    textTransform: 'uppercase',
    fontSize: '0.75rem',
    lineHeight: '1rem',
    letterSpacing: '0.05em',
  },
  title: {
    margin: '0.125rem 0 0',
    fontSize: '2rem',
    lineHeight: '2.375rem',
    color: '#f4f4f4',
  },
  metaBlock: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.125rem',
    minWidth: '6rem',
  },
  metaLabel: {
    margin: 0,
    color: '#8d8d8d',
    fontSize: '0.75rem',
    lineHeight: '1rem',
    textTransform: 'uppercase',
    letterSpacing: '0.04em',
  },
  metaValue: {
    margin: 0,
    color: '#f4f4f4',
    fontSize: '1.25rem',
    lineHeight: '1.5rem',
  },
  nextActionBlock: {
    maxWidth: '24rem',
  },
  nextAction: {
    margin: 0,
    color: '#c6c6c6',
    lineHeight: 1.35,
    fontSize: '0.9rem',
  },
}
