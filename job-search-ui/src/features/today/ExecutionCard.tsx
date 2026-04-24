import type { CSSProperties } from 'react'

type ExecutionCardProps = {
  priority: number
  actionType: string
  title: string
  targetLabel: string
  whyNow: string
  primaryCta: string
  secondaryActions: string[]
}

export function ExecutionCard({
  priority,
  actionType,
  title,
  targetLabel,
  whyNow,
  primaryCta,
  secondaryActions,
}: ExecutionCardProps) {
  return (
    <article style={styles.card}>
      <div style={styles.topRow}>
        <span style={styles.priority}>Priority {priority}</span>
        <span style={styles.actionType}>{actionType.replaceAll('_', ' ')}</span>
      </div>
      <h3 style={styles.title}>{title}</h3>
      <p style={styles.targetLabel}>{targetLabel}</p>
      <p style={styles.whyNow}>{whyNow}</p>
      <div style={styles.buttonRow}>
        <button style={styles.primaryButton} type="button">
          {primaryCta}
        </button>
        {secondaryActions.map((label) => (
          <button key={label} style={styles.secondaryButton} type="button">
            {label}
          </button>
        ))}
      </div>
    </article>
  )
}

const styles: Record<string, CSSProperties> = {
  card: {
    border: '1px solid #1e293b',
    backgroundColor: '#111827',
    borderRadius: '0.75rem',
    padding: '1rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  topRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '1rem',
    fontSize: '0.85rem',
    textTransform: 'uppercase',
    letterSpacing: '0.04em',
  },
  priority: {
    color: '#fbbf24',
    fontWeight: 700,
  },
  actionType: {
    color: '#93c5fd',
  },
  title: {
    margin: 0,
    fontSize: '1.15rem',
    color: '#f8fafc',
  },
  targetLabel: {
    margin: 0,
    color: '#cbd5e1',
    fontWeight: 600,
  },
  whyNow: {
    margin: 0,
    color: '#cbd5e1',
    lineHeight: 1.5,
  },
  buttonRow: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.75rem',
  },
  primaryButton: {
    border: 'none',
    borderRadius: '0.5rem',
    padding: '0.7rem 1rem',
    backgroundColor: '#2563eb',
    color: '#fff',
    cursor: 'pointer',
  },
  secondaryButton: {
    border: '1px solid #334155',
    borderRadius: '0.5rem',
    padding: '0.7rem 1rem',
    backgroundColor: 'transparent',
    color: '#cbd5e1',
    cursor: 'pointer',
  },
}
