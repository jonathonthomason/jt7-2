import { useState, type CSSProperties } from 'react'

type ExecutionCardProps = {
  priority: number
  actionType: string
  status: 'critical' | 'high' | 'medium' | 'low'
  title: string
  targetLabel: string
  whyNow: string
  primaryCta: string
  secondaryActions: string[]
  evidenceSummary?: string
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

function channelLabel(actionType: string) {
  if (actionType.includes('reply') || actionType.includes('outreach') || actionType.includes('follow')) return 'Email'
  if (actionType.includes('interview') || actionType.includes('schedule')) return 'Calendar'
  if (actionType.includes('review')) return 'Review queue'
  return 'JT7'
}

function statusColor(status: ExecutionCardProps['status']) {
  if (status === 'critical') return { backgroundColor: '#2d0709', borderColor: '#fa4d56', color: '#ffb3b8' }
  if (status === 'high') return { backgroundColor: '#3d2a00', borderColor: '#f1c21b', color: '#fddc69' }
  if (status === 'medium') return { backgroundColor: '#1c2e1f', borderColor: '#42be65', color: '#a7f0ba' }
  return { backgroundColor: '#262626', borderColor: '#525252', color: '#c6c6c6' }
}

export function ExecutionCard({
  priority,
  actionType,
  status,
  title,
  targetLabel,
  whyNow,
  primaryCta,
  secondaryActions,
  evidenceSummary,
  emphasis = 'secondary',
}: ExecutionCardProps) {
  const [expanded, setExpanded] = useState(false)
  const actionLabel = humanActionLabel(actionType)
  const visibleSecondaryActions = secondaryActions.length >= 2 ? secondaryActions.slice(0, 2) : [...secondaryActions, 'Log note'].slice(0, 2)

  return (
    <article style={{ ...styles.card, ...(emphasis === 'primary' ? styles.cardPrimary : styles.cardSecondary) }}>
      <div style={styles.metaRow}>
        <span style={styles.priorityLabel}>P{priority}</span>
        <span style={styles.channelLabel}>{channelLabel(actionType)}</span>
        <span style={{ ...styles.statusTag, ...statusColor(status) }}>{status}</span>
      </div>
      {actionLabel ? <p style={styles.actionLabel}>{actionLabel}</p> : null}
      <h3 style={{ ...styles.title, ...(emphasis === 'primary' ? styles.titlePrimary : styles.titleSecondary) }}>{title}</h3>
      <p style={styles.targetLabel}>{targetLabel}</p>
      <p style={styles.whyNow}>{shortWhyNow(whyNow)}</p>
      <div style={styles.buttonRow}>
        <button style={styles.primaryButton} type="button">
          {primaryCta}
        </button>
        {visibleSecondaryActions.map((label) => (
          <button key={label} style={styles.secondaryButton} type="button">
            {label}
          </button>
        ))}
      </div>
      <button style={styles.detailToggle} type="button" onClick={() => setExpanded((value) => !value)}>
        {expanded ? 'Hide detail' : 'Show detail'}
      </button>
      {expanded ? (
        <section style={styles.detailBlock}>
          <p style={styles.detailText}>{whyNow}</p>
          {evidenceSummary ? <p style={styles.detailText}>Evidence: {evidenceSummary}</p> : null}
          <details style={styles.composer}>
            <summary style={styles.composerSummary}>Inline composer</summary>
            <textarea style={styles.textarea} placeholder="Draft response or log note…" />
            <button style={styles.secondaryButton} type="button">Send/log</button>
          </details>
        </section>
      ) : null}
    </article>
  )
}

const styles: Record<string, CSSProperties> = {
  card: {
    border: '1px solid #2a2f3a',
    borderLeft: '3px solid #0f62fe',
    backgroundColor: '#161616',
    borderRadius: 0,
    padding: '0.75rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  cardPrimary: {
    padding: '0.875rem',
    backgroundColor: '#0b0f17',
    borderLeftColor: '#78a9ff',
  },
  cardSecondary: {
    padding: '0.75rem',
  },
  metaRow: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.375rem',
    alignItems: 'center',
  },
  priorityLabel: {
    border: '1px solid #0f62fe',
    borderRadius: 0,
    padding: '0.15rem 0.4rem',
    color: '#78a9ff',
    backgroundColor: '#001d6c',
    fontSize: '0.72rem',
    fontWeight: 700,
  },
  channelLabel: {
    border: '1px solid #393939',
    color: '#c6c6c6',
    backgroundColor: '#262626',
    padding: '0.15rem 0.4rem',
    fontSize: '0.72rem',
  },
  statusTag: {
    border: '1px solid',
    borderRadius: 0,
    padding: '0.15rem 0.4rem',
    fontSize: '0.68rem',
    textTransform: 'uppercase',
    fontWeight: 700,
  },
  actionLabel: {
    margin: 0,
    color: '#33b1ff',
    fontSize: '0.75rem',
    fontWeight: 600,
  },
  title: {
    margin: 0,
    color: '#f4f4f4',
    lineHeight: 1.25,
  },
  titlePrimary: {
    fontSize: '1.125rem',
  },
  titleSecondary: {
    fontSize: '1rem',
  },
  targetLabel: {
    margin: 0,
    color: '#c6c6c6',
    fontWeight: 600,
    fontSize: '0.86rem',
  },
  whyNow: {
    margin: 0,
    color: '#8d8d8d',
    lineHeight: 1.35,
    fontSize: '0.84rem',
  },
  buttonRow: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.5rem',
    marginTop: '0.125rem',
  },
  primaryButton: {
    border: 'none',
    borderRadius: 0,
    padding: '0.5rem 0.85rem',
    backgroundColor: '#0f62fe',
    color: '#ffffff',
    cursor: 'pointer',
    fontWeight: 700,
  },
  secondaryButton: {
    border: '1px solid #393939',
    borderRadius: 0,
    padding: '0.48rem 0.75rem',
    backgroundColor: '#262626',
    color: '#f4f4f4',
    cursor: 'pointer',
  },
  detailToggle: {
    alignSelf: 'flex-start',
    border: 'none',
    backgroundColor: 'transparent',
    color: '#78a9ff',
    padding: 0,
    cursor: 'pointer',
    fontSize: '0.8rem',
  },
  detailBlock: {
    borderTop: '1px solid #262626',
    paddingTop: '0.5rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  detailText: {
    margin: 0,
    color: '#c6c6c6',
    lineHeight: 1.4,
    fontSize: '0.84rem',
  },
  composer: {
    border: '1px solid #393939',
    borderRadius: 0,
    padding: '0.5rem',
    backgroundColor: '#1f1f1f',
  },
  composerSummary: {
    color: '#f4f4f4',
    cursor: 'pointer',
    fontWeight: 600,
    fontSize: '0.84rem',
  },
  textarea: {
    width: '100%',
    minHeight: '4rem',
    margin: '0.5rem 0',
    boxSizing: 'border-box',
    border: '1px solid #393939',
    borderRadius: 0,
    backgroundColor: '#0b0f17',
    color: '#e0e0e0',
    padding: '0.5rem',
    resize: 'vertical',
  },
}
