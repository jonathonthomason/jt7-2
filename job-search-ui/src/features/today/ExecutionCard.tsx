import type { CSSProperties } from 'react'

type ExecutionCardProps = {
  priority: number
  actionType: string
  title: string
  targetLabel: string
  whyNow: string
  primaryCta: string
  secondaryActions: string[]
  emphasis?: 'primary' | 'secondary'
}

function humanActionLabel(actionType: string) {
  if (actionType.includes('review')) return 'Needs review'
  if (actionType.includes('reply') || actionType.includes('outreach')) return 'Reply needed'
  if (actionType.includes('follow')) return 'Follow up'
  if (actionType.includes('interview')) return 'Interview'
  return ''
}

function shortWhyNow(whyNow: string) {
  if (!whyNow) return ''

  const normalized = whyNow
    .replace('This signal was preserved but blocked from job creation. It needs an operator review before tracker mutation.', 'Review before creating job')
    .replace('JT7 has a live next step for this job: ', '')
    .replace('This signal is linked to a real job and is ready for the next operator move.', 'Ready for next step')

  return normalized.length > 72 ? `${normalized.slice(0, 72).trim()}…` : normalized
}

export function ExecutionCard({
  actionType,
  title,
  targetLabel,
  whyNow,
  primaryCta,
  secondaryActions,
  emphasis = 'secondary',
}: ExecutionCardProps) {
  const actionLabel = humanActionLabel(actionType)

  return (
    <article style={{ ...styles.card, ...(emphasis === 'primary' ? styles.cardPrimary : styles.cardSecondary) }}>
      {actionLabel ? <p style={styles.actionLabel}>{actionLabel}</p> : null}
      <h3 style={{ ...styles.title, ...(emphasis === 'primary' ? styles.titlePrimary : styles.titleSecondary) }}>{title}</h3>
      <p style={styles.targetLabel}>{targetLabel}</p>
      <p style={styles.whyNow}>{shortWhyNow(whyNow)}</p>
      <div style={styles.buttonRow}>
        <button style={styles.primaryButton} type="button">
          {primaryCta}
        </button>
        {secondaryActions.slice(0, 1).map((label) => (
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
    gap: '0.6rem',
  },
  cardPrimary: {
    padding: '1.1rem',
    backgroundColor: '#0f172a',
  },
  cardSecondary: {
    padding: '0.9rem',
    opacity: 0.94,
  },
  actionLabel: {
    margin: 0,
    color: '#93c5fd',
    fontSize: '0.78rem',
    fontWeight: 600,
  },
  title: {
    margin: 0,
    color: '#f8fafc',
  },
  titlePrimary: {
    fontSize: '1.2rem',
  },
  titleSecondary: {
    fontSize: '1rem',
  },
  targetLabel: {
    margin: 0,
    color: '#cbd5e1',
    fontWeight: 600,
  },
  whyNow: {
    margin: 0,
    color: '#94a3b8',
    lineHeight: 1.4,
    fontSize: '0.92rem',
  },
  buttonRow: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.6rem',
  },
  primaryButton: {
    border: 'none',
    borderRadius: '0.5rem',
    padding: '0.65rem 0.9rem',
    backgroundColor: '#2563eb',
    color: '#fff',
    cursor: 'pointer',
  },
  secondaryButton: {
    border: '1px solid #334155',
    borderRadius: '0.5rem',
    padding: '0.6rem 0.85rem',
    backgroundColor: 'transparent',
    color: '#cbd5e1',
    cursor: 'pointer',
  },
}
