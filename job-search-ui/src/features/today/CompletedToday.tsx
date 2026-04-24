import type { CSSProperties } from 'react'
import type { ExecutionCardItem } from '../../data/selectors'

type CompletedTodayProps = {
  items: ExecutionCardItem[]
}

export function CompletedToday({ items }: CompletedTodayProps) {
  return (
    <section style={styles.wrap}>
      <h2 style={styles.title}>Completed today</h2>
      {items.length === 0 ? (
        <p style={styles.empty}>Nothing marked completed yet.</p>
      ) : (
        <ul style={styles.list}>
          {items.map((item) => (
            <li key={item.id} style={styles.item}>
              <strong>{item.title}</strong>
              <span style={styles.meta}>{item.targetLabel}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

const styles: Record<string, CSSProperties> = {
  wrap: {
    border: '1px solid #1e293b',
    backgroundColor: '#111827',
    borderRadius: '0.75rem',
    padding: '1rem',
  },
  title: {
    margin: '0 0 0.75rem',
    color: '#f8fafc',
  },
  empty: {
    margin: 0,
    color: '#94a3b8',
  },
  list: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  item: {
    display: 'flex',
    justifyContent: 'space-between',
    gap: '1rem',
    color: '#e2e8f0',
  },
  meta: {
    color: '#94a3b8',
  },
}
