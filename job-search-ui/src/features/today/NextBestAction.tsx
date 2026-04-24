import type { ExecutionCardItem } from '../../data/selectors'
import { ExecutionCard } from './ExecutionCard'

type NextBestActionProps = {
  item: ExecutionCardItem | null
}

export function NextBestAction({ item }: NextBestActionProps) {
  if (!item) return null

  return (
    <section>
      <p style={{ margin: '0 0 0.5rem', color: '#93c5fd', textTransform: 'uppercase', fontSize: '0.78rem', letterSpacing: '0.04em' }}>
        Start here
      </p>
      <ExecutionCard {...item} emphasis="primary" />
    </section>
  )
}
