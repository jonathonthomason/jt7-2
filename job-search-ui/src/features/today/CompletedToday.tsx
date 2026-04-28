import type { CSSProperties } from 'react'
import type { ExecutionCardItem } from '../../data/selectors'

type CompletedTodayProps = {
  items: ExecutionCardItem[]
}

export function CompletedToday({ items }: CompletedTodayProps) {
  if (items.length === 0) return null

  return (
    <section style={styles.wrap}>
      <h2 style={styles.title}>Completed today</h2>
      <ul style={styles.list}>
        {items.map((item) => (
          <li key={item.id} style={styles.item}>
            <strong>{item.title}</strong>
            <span style={styles.meta}>{item.targetLabel}</span>
          </li>
        ))}
      </ul>
    </section>
  )
}

const styles: Record<string, CSSProperties> = {
  wrap: {
    border: '1px solid #2a2f3a',
    backgroundColor: '#161616',
    borderRadius: 0,
    padding: '0.75rem',
  },
  title: {
    margin: '0 0 0.5rem',
    color: '#f4f4f4',
    fontSize: '0.95rem',
    lineHeight: '1.25rem',
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
    gap: '0.5rem',
  },
  item: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    gap: '0.15rem',
    color: '#e0e0e0',
    borderTop: '1px solid #262626',
    paddingTop: '0.5rem',
    fontSize: '0.85rem',
  },
  meta: {
    color: '#8d8d8d',
  },
}
