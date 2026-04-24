import type { ExecutionCardItem } from '../../data/selectors'
import { ExecutionCard } from './ExecutionCard'

type NextBestActionProps = {
  item: ExecutionCardItem | null
}

export function NextBestAction({ item }: NextBestActionProps) {
  if (!item) return null

  return (
    <section>
      <p style={{ margin: '0 0 0.75rem', color: '#93c5fd', textTransform: 'uppercase', fontSize: '0.8rem' }}>
        Next best action
      </p>
      <ExecutionCard {...item} />
    </section>
  )
}
