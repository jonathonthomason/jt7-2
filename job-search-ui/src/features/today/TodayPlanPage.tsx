import type { CSSProperties } from 'react'
import {
  getCompletedToday,
  getExecutionCards,
  getNextBestAction,
  getRecentSignals,
  getTodayPlanSummary,
  getWaitingActions,
} from '../../data/selectors'
import { CompletedToday } from './CompletedToday'
import { ExecutionCard } from './ExecutionCard'
import { NextBestAction } from './NextBestAction'
import { ProgressStrip } from './ProgressStrip'

export function TodayPlanPage() {
  const summary = getTodayPlanSummary()
  const nextBestAction = getNextBestAction()
  const executionCards = getExecutionCards().slice(0, 5)
  const completedToday = getCompletedToday()
  const recentSignals = getRecentSignals()
  const waitingActions = getWaitingActions()

  return (
    <section style={styles.page}>
      <ProgressStrip summary={summary} />
      <section style={styles.operatorBand} aria-label="Operator band">
        <div>
          <p style={styles.kicker}>Operator</p>
          <strong style={styles.operatorStatus}>Ready for sweep</strong>
        </div>
        <div style={styles.operatorActions}>
          <button style={styles.secondaryButton} type="button">Run sweep</button>
          <button style={styles.secondaryButton} type="button">Refresh</button>
          <span style={styles.signalPill}>{recentSignals.length} signals</span>
        </div>
      </section>
      <div style={styles.workspaceGrid}>
        <main style={styles.primaryColumn}>
          <NextBestAction item={nextBestAction} />
          <section style={styles.section}>
            <div style={styles.list}>
              {executionCards.map((item) => (
                <ExecutionCard key={item.id} {...item} emphasis="secondary" />
              ))}
            </div>
          </section>
          <details style={styles.whyBlock}>
            <summary style={styles.summary}>Why this plan</summary>
            <p style={styles.muted}>{summary.operatorSummary}. Next action: {summary.nextBestActionTitle}.</p>
          </details>
        </main>
        <aside style={styles.sideColumn}>
          {recentSignals.length > 0 ? (
            <section style={styles.sectionCard}>
              <div style={styles.sectionHeader}>
                <h2 style={styles.sectionTitle}>Signals</h2>
                <span style={styles.countTag}>{recentSignals.length}</span>
              </div>
              <div style={styles.signalGrid}>
                {recentSignals.map((item) => (
                  <article key={item.id} style={styles.signalCard}>
                    <div style={styles.signalTopRow}>
                      <span style={styles.signalType}>{item.signalType}</span>
                      <span style={styles.signalSource}>mirror</span>
                    </div>
                    <strong style={styles.signalSummary}>{item.company}</strong>
                    <p style={styles.signalMeta}>{item.timestamp}</p>
                    <button style={styles.signalAction} type="button">Inspect</button>
                  </article>
                ))}
              </div>
            </section>
          ) : null}
          <section style={styles.sectionCard}>
            <div style={styles.sectionHeader}>
              <h2 style={styles.sectionTitle}>Waiting</h2>
              <span style={styles.countTag}>{waitingActions.length}</span>
            </div>
            {waitingActions.length > 0 ? (
              <ul style={styles.simpleList}>
                {waitingActions.slice(0, 4).map((item) => (
                  <li key={item.id} style={styles.simpleItem}>
                    <strong style={styles.simpleTitle}>{item.title}</strong>
                    <span style={styles.muted}>{item.targetLabel}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p style={styles.muted}>No waiting items staged.</p>
            )}
          </section>
          <CompletedToday items={completedToday} />
        </aside>
      </div>
    </section>
  )
}

const styles: Record<string, CSSProperties> = {
  page: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
    textAlign: 'left',
  },
  operatorBand: {
    border: '1px solid #2a2f3a',
    borderLeft: '3px solid #0f62fe',
    backgroundColor: '#161616',
    borderRadius: 0,
    padding: '0.75rem 1rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: '0.75rem',
    flexWrap: 'wrap',
  },
  kicker: {
    margin: 0,
    color: '#78a9ff',
    textTransform: 'uppercase',
    fontSize: '0.75rem',
    lineHeight: '1rem',
    letterSpacing: '0.06em',
  },
  operatorStatus: {
    color: '#f4f4f4',
    fontSize: '0.95rem',
  },
  operatorActions: {
    display: 'flex',
    gap: '0.5rem',
    flexWrap: 'wrap',
    alignItems: 'center',
  },
  secondaryButton: {
    border: '1px solid #393939',
    borderRadius: 0,
    padding: '0.4rem 0.75rem',
    backgroundColor: '#262626',
    color: '#f4f4f4',
    cursor: 'pointer',
    fontSize: '0.82rem',
  },
  signalPill: {
    border: '1px solid #393939',
    padding: '0.35rem 0.65rem',
    backgroundColor: '#0f172a',
    color: '#c6c6c6',
    fontSize: '0.78rem',
  },
  workspaceGrid: {
    display: 'grid',
    gridTemplateColumns: 'minmax(0, 1fr) 320px',
    gap: '0.75rem',
    alignItems: 'start',
  },
  primaryColumn: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  sideColumn: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  section: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  whyBlock: {
    border: '1px solid #2a2f3a',
    backgroundColor: '#161616',
    borderRadius: 0,
    padding: '0.75rem',
  },
  summary: {
    color: '#f4f4f4',
    cursor: 'pointer',
    fontWeight: 600,
    fontSize: '0.9rem',
  },
  sectionCard: {
    border: '1px solid #2a2f3a',
    backgroundColor: '#161616',
    borderRadius: 0,
    padding: '0.75rem',
  },
  sectionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '0.5rem',
  },
  sectionTitle: {
    margin: 0,
    color: '#f4f4f4',
    fontSize: '0.95rem',
    lineHeight: '1.25rem',
  },
  countTag: {
    border: '1px solid #393939',
    color: '#c6c6c6',
    backgroundColor: '#262626',
    padding: '0.1rem 0.45rem',
    fontSize: '0.72rem',
  },
  simpleList: {
    listStyle: 'none',
    margin: 0,
    padding: 0,
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  simpleItem: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    gap: '0.15rem',
    color: '#e0e0e0',
    borderTop: '1px solid #262626',
    paddingTop: '0.5rem',
  },
  simpleTitle: {
    fontSize: '0.85rem',
    lineHeight: 1.35,
  },
  muted: {
    margin: 0,
    color: '#8d8d8d',
    fontSize: '0.82rem',
    lineHeight: 1.4,
  },
  signalGrid: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  signalCard: {
    border: '1px solid #393939',
    borderLeft: '3px solid #33b1ff',
    borderRadius: 0,
    padding: '0.6rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.35rem',
    color: '#e0e0e0',
    backgroundColor: '#1f1f1f',
  },
  signalTopRow: {
    display: 'flex',
    justifyContent: 'space-between',
    gap: '0.5rem',
    alignItems: 'center',
  },
  signalType: {
    color: '#33b1ff',
    textTransform: 'uppercase',
    fontSize: '0.68rem',
    letterSpacing: '0.05em',
  },
  signalSource: {
    color: '#c6c6c6',
    backgroundColor: '#262626',
    padding: '0.05rem 0.35rem',
    fontSize: '0.68rem',
  },
  signalSummary: {
    color: '#f4f4f4',
    fontSize: '0.9rem',
    lineHeight: 1.25,
  },
  signalMeta: {
    margin: 0,
    color: '#8d8d8d',
    fontSize: '0.75rem',
  },
  signalAction: {
    alignSelf: 'flex-start',
    border: '1px solid #393939',
    borderRadius: 0,
    padding: '0.3rem 0.55rem',
    backgroundColor: '#262626',
    color: '#f4f4f4',
    cursor: 'pointer',
    fontSize: '0.75rem',
  },
}
