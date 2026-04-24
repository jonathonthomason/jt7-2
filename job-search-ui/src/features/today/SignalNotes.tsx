import type { CSSProperties } from 'react'
import type { RecentSignalItem } from '../../data/selectors'

type SignalNotesProps = {
  items: RecentSignalItem[]
}

export function SignalNotes({ items }: SignalNotesProps) {
  return (
    <section style={styles.wrap}>
      <h2 style={styles.title}>Signal notes</h2>
      <ul style={styles.list}>
        {items.map((item) => (
          <li key={item.id} style={styles.item}>
            <span style={styles.type}>{item.signalType}</span>
            <span style={styles.company}>{item.company}</span>
            <span style={styles.timestamp}>{item.timestamp}</span>
          </li>
        ))}
      </ul>
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
  list: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  item: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr auto',
    gap: '1rem',
    color: '#e2e8f0',
  },
  type: {
    color: '#93c5fd',
  },
  company: {
    color: '#e2e8f0',
  },
  timestamp: {
    color: '#94a3b8',
    fontSize: '0.85rem',
  },
}
