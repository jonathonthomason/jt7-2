import type { CSSProperties, ReactNode } from 'react'
import { useMvpState, type MvpAction, type MvpSignal } from '../../state/mvpState'
import type { ReviewItem, StagedOpportunity } from '../../domain/cockpit/types'

function SectionTitle({ title, count }: { title: string; count?: number }) {
  return <div style={styles.sectionHeader}><h2 style={styles.sectionTitle}>{title}</h2>{count !== undefined ? <span style={styles.countTag}>{count}</span> : null}</div>
}

function StatusTag({ value }: { value: string }) {
  const lower = value.toLowerCase()
  const color = lower.includes('reject') || lower.includes('blocked') || lower.includes('dismiss') ? '#fa4d56' : lower.includes('waiting') || lower.includes('review') || lower.includes('pending') || lower.includes('defer') ? '#f1c21b' : lower.includes('done') || lower.includes('applied') || lower.includes('active') || lower.includes('confirm') || lower.includes('link') ? '#42be65' : '#78a9ff'
  return <span style={{ ...styles.tag, borderColor: color, color }}>{value}</span>
}

function confidenceLabel(value: number) {
  if (value >= 0.75) return 'high confidence'
  if (value >= 0.5) return 'medium confidence'
  return 'low confidence'
}

export function ReviewQueueCard({ item }: { item: ReviewItem }) {
  const { openPanel, reviewCommand } = useMvpState()
  return (
    <article style={styles.reviewCard}>
      <div style={styles.rowBetween}>
        <div style={styles.tagRow}>
          <span style={styles.priorityTag}>{item.priority.toUpperCase()}</span>
          <StatusTag value={item.status} />
          <span style={styles.tag}>{confidenceLabel(item.confidence)}</span>
        </div>
        <button style={styles.linkButton} onClick={() => openPanel('review', item.id)} type="button">Detail</button>
      </div>
      <h3 style={styles.actionTitle}>{item.extractedRole || 'Unknown role'}</h3>
      <p style={styles.meta}>{item.extractedCompany || 'Unknown company'} · {item.source}</p>
      <p style={styles.copy}>{item.evidenceSummary}</p>
      <p style={styles.meta}>Reason: {item.reasonForReview}</p>
      <div style={styles.buttonRow}>
        <button style={styles.primaryButton} onClick={() => reviewCommand(item.id, 'Confirm')} type="button">Confirm</button>
        <button style={styles.secondaryButton} onClick={() => reviewCommand(item.id, 'Link')} type="button">Link</button>
        <button style={styles.secondaryButton} onClick={() => reviewCommand(item.id, 'Dismiss')} type="button">Dismiss</button>
        <button style={styles.secondaryButton} onClick={() => reviewCommand(item.id, 'Defer')} type="button">Defer</button>
      </div>
    </article>
  )
}

export function ReviewQueuePage() {
  const { reviewSummary, state, openPanel } = useMvpState()
  return (
    <section style={styles.page}>
      <section style={styles.hero}>
        <div>
          <p style={styles.kicker}>Trust / Review Queue</p>
          <h1 style={styles.title}>Review Queue</h1>
          <p style={styles.copy}>Signals are untrusted on arrival. Review determines what becomes real pipeline state.</p>
        </div>
        <div>
          <p style={styles.meta}>Pending</p>
          <strong>{reviewSummary.pending.length}</strong>
        </div>
        <div>
          <p style={styles.meta}>High priority</p>
          <strong>{reviewSummary.highPriority.length}</strong>
        </div>
      </section>
      <div style={styles.grid}>
        <main style={styles.stack}>
          <SectionTitle title="Pending reviews" count={reviewSummary.pending.length} />
          <div style={styles.stack}>
            {reviewSummary.pending.slice(0, 12).map((item) => <ReviewQueueCard key={item.id} item={item} />)}
          </div>
        </main>
        <aside style={styles.stack}>
          <section style={styles.tile}>
            <SectionTitle title="High-priority queue" count={reviewSummary.highPriority.length} />
            <ul style={styles.cleanList}>
              {reviewSummary.highPriority.slice(0, 8).map((item) => (
                <li key={item.id} style={styles.listItem}>
                  <button style={styles.linkButton} onClick={() => openPanel('review', item.id)} type="button">{item.extractedCompany || 'Unknown company'} — {item.extractedRole || 'Unknown role'}</button>
                  <span style={styles.meta}>{item.reasonForReview}</span>
                </li>
              ))}
            </ul>
          </section>
          <section style={styles.tile}>
            <SectionTitle title="Recent review events" count={state.reviewEvents.length} />
            {state.reviewEvents.length ? (
              <ul style={styles.cleanList}>
                {state.reviewEvents.slice(0, 8).map((event) => (
                  <li key={event.id} style={styles.listItem}>
                    <span>{event.command}</span>
                    <span style={styles.meta}>{event.reviewId} · {event.timestamp}</span>
                  </li>
                ))}
              </ul>
            ) : <p style={styles.meta}>No review actions recorded yet.</p>}
          </section>
        </aside>
      </div>
    </section>
  )
}

function FitTag({ value }: { value: StagedOpportunity['fitBand'] }) {
  const color = value === 'strong' ? '#42be65' : value === 'maybe' ? '#f1c21b' : '#fa4d56'
  return <span style={{ ...styles.tag, borderColor: color, color }}>{value}</span>
}

function DuplicateTag({ item }: { item: StagedOpportunity }) {
  if (!item.duplicateMatches?.length) return null
  return <span style={{ ...styles.tag, borderColor: '#fa4d56', color: '#fa4d56' }}>{item.duplicateMatches.length} canonical match{item.duplicateMatches.length > 1 ? 'es' : ''}</span>
}

function writebackState(item: StagedOpportunity): { tone: 'success' | 'error' | 'neutral'; text: string } | null {
  const notes = item.notes || ''
  if (notes.includes('Writeback failed:')) {
    const detail = notes.split('Writeback failed:').pop()?.trim() || 'Runtime writeback failed'
    return { tone: 'error', text: `Writeback failed · ${detail}` }
  }
  if (notes.includes('Runtime created via')) return { tone: 'success', text: 'Canonical create applied' }
  if (notes.includes('Runtime merged via')) return { tone: 'success', text: 'Canonical merge applied' }
  if (item.status === 'hold') return { tone: 'neutral', text: 'Held for manual review' }
  if (item.status === 'reject') return { tone: 'error', text: 'Rejected from canonical promotion' }
  return null
}

function StagingCard({ item }: { item: StagedOpportunity }) {
  const { openPanel, stagingCommand } = useMvpState()
  const writeback = writebackState(item)
  return (
    <article style={styles.reviewCard}>
      <div style={styles.rowBetween}>
        <div style={styles.tagRow}>
          <FitTag value={item.fitBand} />
          <StatusTag value={item.status} />
          <span style={styles.tag}>score {item.fitScore ?? 0}</span>
          <span style={styles.tag}>{item.sourceBoard}</span>
          <span style={styles.tag}>{item.duplicateRisk} duplicate risk</span>
          <DuplicateTag item={item} />
        </div>
        <button style={styles.linkButton} onClick={() => openPanel('staging', item.id)} type="button">Detail</button>
      </div>
      <h3 style={styles.actionTitle}>{item.role}</h3>
      <p style={styles.meta}>{item.company} · {item.location}</p>
      <p style={styles.copy}>{item.recommendedAction}</p>
      <p style={styles.meta}>Why: {item.reasons.join(' · ')}</p>
      {writeback ? <p style={{ ...styles.meta, color: writeback.tone === 'success' ? '#42be65' : writeback.tone === 'error' ? '#fa4d56' : '#c6c6c6' }}>{writeback.text}</p> : null}
      {item.duplicateMatches?.length ? <p style={styles.meta}>Canonical matches: {item.duplicateMatches.join(', ')}</p> : null}
      <div style={styles.buttonRow}>
        {item.duplicateMatches?.length ? <button style={styles.primaryButton} onClick={() => stagingCommand(item.id, 'Merge')} type="button">Merge</button> : <button style={styles.primaryButton} onClick={() => stagingCommand(item.id, 'Promote')} type="button">Promote</button>}
        <button style={styles.secondaryButton} onClick={() => stagingCommand(item.id, 'Hold')} type="button">Hold</button>
        <button style={styles.secondaryButton} onClick={() => stagingCommand(item.id, 'Reject')} type="button">Reject</button>
      </div>
    </article>
  )
}

export function StagingIntakePage() {
  const { stagingSummary, state, openPanel, stagingCommand } = useMvpState()
  const promotedCount = state.stagingQueue.filter((item) => writebackState(item)?.tone === 'success').length
  const failedCount = state.stagingQueue.filter((item) => writebackState(item)?.tone === 'error' && (item.notes || '').includes('Writeback failed:')).length
  const duplicateCandidates = state.stagingQueue.filter((item) => item.duplicateMatches?.length)
  return (
    <section style={styles.page}>
      <section style={styles.hero}>
        <div>
          <p style={styles.kicker}>Trust / Staging</p>
          <h1 style={styles.title}>Staging Intake</h1>
          <p style={styles.copy}>Broad board imports land here first. Nothing in this view is canonical tracker truth until it is intentionally promoted.</p>
        </div>
        <div>
          <p style={styles.meta}>Pending staged</p>
          <strong>{stagingSummary.pending.length}</strong>
        </div>
        <div>
          <p style={styles.meta}>Strong fit</p>
          <strong>{stagingSummary.strongFit.length}</strong>
        </div>
        <div>
          <p style={styles.meta}>Writebacks</p>
          <strong>{promotedCount}</strong>
          <p style={styles.meta}>{failedCount ? `${failedCount} failed` : '0 failed'}</p>
        </div>
      </section>
      <div style={styles.grid}>
        <main style={styles.stack}>
          <SectionTitle title="Pending staging review" count={stagingSummary.pending.length} />
          <div style={styles.stack}>
            {stagingSummary.pending.slice(0, 16).map((item) => <StagingCard key={item.id} item={item} />)}
          </div>
        </main>
        <aside style={styles.stack}>
          <section style={styles.tile}>
            <SectionTitle title="Promotion candidates" count={stagingSummary.strongFit.length} />
            <ul style={styles.cleanList}>
              {stagingSummary.strongFit.slice(0, 8).map((item) => (
                <li key={item.id} style={styles.listItem}>
                  <button style={styles.linkButton} onClick={() => openPanel('staging', item.id)} type="button">{item.company} — {item.role}</button>
                  <span style={styles.meta}>{item.location} · score {item.fitScore ?? 0}</span>
                </li>
              ))}
            </ul>
          </section>
          <section style={styles.tile}>
            <SectionTitle title="Duplicate candidates" count={duplicateCandidates.length} />
            {duplicateCandidates.length ? (
              <ul style={styles.cleanList}>
                {duplicateCandidates.slice(0, 8).map((item) => (
                  <li key={item.id} style={styles.listItem}>
                    <button style={styles.linkButton} onClick={() => openPanel('staging', item.id)} type="button">{item.company} — {item.role}</button>
                    <span style={styles.meta}>{item.duplicateMatches?.join(', ')} · score {item.fitScore ?? 0}</span>
                    <div style={styles.buttonRow}>
                      <button style={styles.primaryButton} onClick={() => stagingCommand(item.id, 'Merge')} type="button">Merge duplicate</button>
                      <button style={styles.secondaryButton} onClick={() => openPanel('staging', item.id)} type="button">Inspect</button>
                    </div>
                  </li>
                ))}
              </ul>
            ) : <p style={styles.meta}>No duplicate candidates currently surfaced.</p>}
          </section>
          <section style={styles.tile}>
            <SectionTitle title="Trust boundary" />
            <ul style={styles.cleanList}>
              <li style={styles.listItem}>Canonical Jobs remain trusted tracker state.</li>
              <li style={styles.listItem}>Staged imports keep board provenance, fit score, and duplicate risk visible.</li>
              <li style={styles.listItem}>Only explicit promotion should create or update tracker-facing jobs.</li>
              <li style={styles.listItem}>Current staged corpus: {state.stagingQueue.length} imported roles.</li>
              <li style={styles.listItem}>Potential canonical duplicates currently flagged: {state.stagingQueue.filter((item) => item.duplicateMatches?.length).length}.</li>
            </ul>
          </section>
        </aside>
      </div>
    </section>
  )
}

export function SignalCard({ signal }: { signal: MvpSignal }) {
  const { openPanel, signalCommand } = useMvpState()
  return (
    <article style={styles.signalCard}>
      <div style={styles.rowBetween}><span style={styles.kicker}>{signal.type}</span><StatusTag value={signal.priority} /></div>
      <strong style={styles.cardTitle}>{signal.company}</strong>
      <p style={styles.meta}>{signal.source} · {signal.timestamp}</p>
      <p style={styles.copy}>{signal.summary}</p>
      <div style={styles.buttonRow}>
        <button style={styles.primaryButton} onClick={() => signalCommand(signal.id, 'Create Action')} type="button">Create Action</button>
        <button style={styles.secondaryButton} onClick={() => openPanel('signal', signal.id)} type="button">Inspect</button>
        <button style={styles.secondaryButton} onClick={() => signalCommand(signal.id, 'Dismiss')} type="button">Dismiss</button>
      </div>
    </article>
  )
}

export function MvpExecutionCard({ action, emphasis = 'secondary' }: { action: MvpAction; emphasis?: 'primary' | 'secondary' }) {
  const { actionCommand, openPanel } = useMvpState()
  return (
    <article style={{ ...styles.executionCard, ...(emphasis === 'primary' ? styles.executionPrimary : {}) }}>
      <div style={styles.rowBetween}>
        <div style={styles.tagRow}><span style={styles.priorityTag}>P{action.priority}</span><span style={styles.tag}>{action.channel}</span><StatusTag value={action.status} /></div>
        <button style={styles.linkButton} onClick={() => openPanel('action', action.id)} type="button">Detail</button>
      </div>
      <h3 style={styles.actionTitle}>{action.title}</h3>
      <p style={styles.meta}>{action.target} · {action.company}</p>
      <p style={styles.copy}>{action.whyNow}</p>
      <div style={styles.buttonRow}>
        <button style={styles.primaryButton} onClick={() => actionCommand(action.id, action.primaryCta)} type="button">{action.primaryCta}</button>
        <button style={styles.secondaryButton} onClick={() => actionCommand(action.id, 'Mark Waiting')} type="button">Waiting</button>
        <button style={styles.secondaryButton} onClick={() => actionCommand(action.id, 'Defer')} type="button">Defer</button>
        <button style={styles.secondaryButton} onClick={() => actionCommand(action.id, 'Complete')} type="button">Complete</button>
      </div>
      <details style={styles.details}>
        <summary>Inline composer</summary>
        <textarea style={styles.textarea} placeholder="Draft, reply, or log note…" onBlur={(event) => actionCommand(action.id, 'Log Note', event.currentTarget.value)} />
      </details>
    </article>
  )
}

export function TodayPlanPage() {
  const { today, state, runSweep, refreshPlan, reviewSummary } = useMvpState()
  return (
    <section style={styles.page}>
      <section style={styles.hero}>
        <div><p style={styles.kicker}>/execute/today</p><h1 style={styles.title}>Today’s Plan</h1></div>
        <div><p style={styles.meta}>Progress</p><strong>{today.completedCount}/{today.totalCount}</strong></div>
        <div><p style={styles.meta}>Review backlog</p><p style={styles.copy}>{reviewSummary.pending.length} pending review items</p></div>
      </section>
      <section style={styles.operatorBand}>
        <div><p style={styles.kicker}>Operator Band</p><strong>{today.latestRun?.status ?? 'ready'}</strong><p style={styles.meta}>{today.latestRun?.lastRunAt ?? state.lastUpdated}</p></div>
        <div style={styles.buttonRow}><button style={styles.primaryButton} onClick={runSweep} type="button">Run Sweep</button><button style={styles.secondaryButton} onClick={refreshPlan} type="button">Refresh</button><span style={styles.tag}>{today.newSignals.length} new signals</span></div>
      </section>
      <div style={styles.grid}>
        <main style={styles.stack}>
          {today.nextAction ? <MvpExecutionCard action={today.nextAction} emphasis="primary" /> : null}
          <SectionTitle title="Execution Cards" count={today.openActions.length} />
          <div style={styles.stack}>{today.openActions.map((action) => <MvpExecutionCard key={action.id} action={action} />)}</div>
          <details style={styles.tile}><summary style={styles.summary}>Why this plan</summary><p style={styles.copy}>Ranked from open/blocked actions, pending reviews, recent recruiter/job signals, urgency, and current action state. Latest run: {today.latestRun?.summary ?? 'local state only'}.</p></details>
        </main>
        <aside style={styles.stack}>
          <section style={styles.tile}><SectionTitle title="New Signals" count={today.newSignals.length} /><div style={styles.stack}>{today.newSignals.slice(0, 5).map((signal) => <SignalCard key={signal.id} signal={signal} />)}</div></section>
          <section style={styles.tile}><SectionTitle title="Waiting / Deferred" count={today.waitingActions.length} /><CompactActionList actions={today.waitingActions} /></section>
          <section style={styles.tile}><SectionTitle title="Completed Today" count={today.completedToday.length} /><CompactActionList actions={today.completedToday} /></section>
        </aside>
      </div>
    </section>
  )
}

function CompactActionList({ actions }: { actions: MvpAction[] }) {
  const { openPanel } = useMvpState()
  if (!actions.length) return <p style={styles.meta}>None.</p>
  return <ul style={styles.cleanList}>{actions.slice(0, 8).map((action) => <li key={action.id} style={styles.listItem}><button style={styles.linkButton} onClick={() => openPanel('action', action.id)} type="button">{action.title}</button><span style={styles.meta}>{action.company}</span></li>)}</ul>
}

export function JobsPage() {
  const { state, openPanel, jobCommand } = useMvpState()
  return <TablePage title="Jobs" rows={state.jobs} renderHeader={() => <tr><Th>Role</Th><Th>Company</Th><Th>Status</Th><Th>Source</Th><Th>Priority</Th><Th>Date found</Th><Th>Next action</Th><Th>Recruiter</Th><Th>Link</Th><Th>Actions</Th></tr>} renderRow={(job) => <tr key={job.id}><Td>{job.role}</Td><Td>{job.company}</Td><Td><StatusTag value={job.status} /></Td><Td>{job.source}</Td><Td>{job.priority}</Td><Td>{job.dateFound}</Td><Td>{job.nextAction}</Td><Td>{job.recruiterName ?? '—'}</Td><Td>{job.link ? <a style={styles.link} href={job.link}>open</a> : '—'}</Td><Td><button style={styles.secondaryButton} onClick={() => jobCommand(job.id, 'Review')} type="button">Review</button><button style={styles.secondaryButton} onClick={() => jobCommand(job.id, 'Apply')} type="button">Apply</button><button style={styles.secondaryButton} onClick={() => jobCommand(job.id, 'Create Follow-up')} type="button">Follow-up</button><button style={styles.secondaryButton} onClick={() => openPanel('job', job.id)} type="button">Detail</button></Td></tr>} />
}

export function RecruitersPage() {
  const { state, openPanel, recruiterCommand } = useMvpState()
  return <TablePage title="Recruiters" rows={state.recruiters} renderHeader={() => <tr><Th>Name</Th><Th>Company/Agency</Th><Th>Status</Th><Th>Last contact</Th><Th>Next action</Th><Th>Related jobs</Th><Th>Actions</Th></tr>} renderRow={(r) => <tr key={r.id}><Td>{r.name}</Td><Td>{r.company}</Td><Td><StatusTag value={r.status} /></Td><Td>{r.lastContact ?? '—'}</Td><Td>{r.nextAction}</Td><Td>{r.relatedJobs.length}</Td><Td><button style={styles.secondaryButton} onClick={() => recruiterCommand(r.id, 'Draft Reply')} type="button">Draft Reply</button><button style={styles.secondaryButton} onClick={() => recruiterCommand(r.id, 'Follow Up')} type="button">Follow Up</button><button style={styles.secondaryButton} onClick={() => openPanel('recruiter', r.id)} type="button">Detail</button></Td></tr>} />
}

export function OutreachPage() {
  const { state } = useMvpState()
  return <TablePage title="Outreach" rows={state.outreach} renderHeader={() => <tr><Th>Contact</Th><Th>Company</Th><Th>Channel</Th><Th>Type</Th><Th>Status</Th><Th>Sent</Th><Th>Follow-up</Th><Th>Related job</Th></tr>} renderRow={(o) => <tr key={o.id}><Td>{o.contact}</Td><Td>{o.company}</Td><Td>{o.channel}</Td><Td>{o.messageType}</Td><Td><StatusTag value={o.status} /></Td><Td>{o.sentDate ?? '—'}</Td><Td>{o.followUpDate ?? '—'}</Td><Td>{o.relatedJob ?? '—'}</Td></tr>} />
}

export function MessagesPage() {
  const { state, openPanel } = useMvpState()
  return <TablePage title="Messages" rows={state.messages} renderHeader={() => <tr><Th>Direction</Th><Th>Contact</Th><Th>Company</Th><Th>Subject</Th><Th>Status</Th><Th>Recommended action</Th><Th>Actions</Th></tr>} renderRow={(m) => <tr key={m.id}><Td>{m.direction}</Td><Td>{m.contact}</Td><Td>{m.company}</Td><Td>{m.subject}</Td><Td><StatusTag value={m.status} /></Td><Td>{m.recommendedAction}</Td><Td><button style={styles.secondaryButton} onClick={() => openPanel('message', m.id)} type="button">Detail</button></Td></tr>} />
}

export function CompetitionPage() {
  const { state } = useMvpState()
  return <SimpleIntelligence title="Competition" items={[`Tracked benchmarks: ${state.competition.length}`, 'Role patterns: senior/principal product design, systems, AI workflows', 'Market signals: recruiter/job-board signals from local mirror', 'Positioning note: emphasize strategic range + execution systems']} />
}

export function WikiPage() {
  return <SimpleIntelligence title="Wiki" items={['Reusable answer: systems-minded product designer', 'Narrative: AI operations + design leadership', 'Framework: signal → review → decision → action → tracker', 'Company research: attach to job detail notes']} />
}

export function ReportsPage() {
  const { state, today, reviewSummary, stagingSummary } = useMvpState()
  return <SimpleIntelligence title="Reports" items={[`Pipeline health: ${state.jobs.length} jobs / ${state.recruiters.length} recruiters`, `Pending reviews: ${reviewSummary.pending.length}`, `Staged intake backlog: ${stagingSummary.pending.length}`, `Promotion candidates: ${stagingSummary.strongFit.length}`, `Recruiter response trend: ${state.messages.filter((m) => m.direction === 'inbound').length} inbound messages`, `Completed actions: ${today.completedToday.length}`, `Weekly summary: ${today.latestRun?.summary ?? 'No run summary'}`]} />
}

export function ComponentsPage() {
  return <SimpleIntelligence title="Design System / Components" items={['Review Queue card: trust state, evidence, decision actions', 'Execution Card: priority, channel, CTA, composer, state mutation', 'Signal Card: source/type/summary/action', 'Operator Band: run status, sweep, refresh, counts', 'Right Detail Panel: persistent, no modal stacks', 'Status Tags: semantic color', 'Data Tables: compact Carbon-like rows', 'Inline Composer: logs notes to local state']} />
}

export function FoundationsPage() {
  return <SimpleIntelligence title="Design System / Foundations" items={['IBM Carbon-inspired, not Carbon package', 'Dark low-glare surfaces: #0b0f17 / #161616 / #262626', 'Blue action, green success, yellow attention, red blocked, cyan system', '8pt grid, dense operator layout', 'Square tiles/tables/buttons, restrained hierarchy']} />
}

export function SettingsPage() {
  const { state, refreshPlan } = useMvpState()
  return <section style={styles.page}><h1 style={styles.title}>Settings</h1><div style={styles.tile}><p style={styles.copy}>Local MVP state is persisted in browser localStorage. Seed source is the repo data mirror.</p><p style={styles.meta}>Last updated: {state.lastUpdated}</p><button style={styles.primaryButton} onClick={refreshPlan} type="button">Refresh state timestamp</button></div></section>
}

function SimpleIntelligence({ title, items }: { title: string; items: string[] }) {
  return <section style={styles.page}><h1 style={styles.title}>{title}</h1><div style={styles.tile}><ul style={styles.cleanList}>{items.map((item) => <li key={item} style={styles.listItem}>{item}</li>)}</ul></div></section>
}

function TablePage<T>({ title, rows, renderHeader, renderRow }: { title: string; rows: T[]; renderHeader: () => ReactNode; renderRow: (row: T) => ReactNode }) {
  return <section style={styles.page}><div style={styles.rowBetween}><h1 style={styles.title}>{title}</h1><span style={styles.countTag}>{rows.length} records</span></div><div style={styles.tableWrap}><table style={styles.table}><thead>{renderHeader()}</thead><tbody>{rows.map(renderRow)}</tbody></table></div></section>
}

function Th({ children }: { children: ReactNode }) { return <th style={styles.th}>{children}</th> }
function Td({ children }: { children: ReactNode }) { return <td style={styles.td}>{children}</td> }

const styles: Record<string, CSSProperties> = {
  page: { display: 'flex', flexDirection: 'column', gap: '0.75rem', textAlign: 'left' },
  hero: { border: '1px solid #2a2f3a', borderTop: '3px solid #0f62fe', backgroundColor: '#161616', padding: '1rem', display: 'grid', gridTemplateColumns: '1fr auto minmax(220px, 320px)', gap: '1rem', alignItems: 'end' },
  operatorBand: { border: '1px solid #2a2f3a', borderLeft: '3px solid #0f62fe', backgroundColor: '#161616', padding: '0.75rem', display: 'flex', justifyContent: 'space-between', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' },
  grid: { display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 340px', gap: '0.75rem', alignItems: 'start' },
  stack: { display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  tile: { border: '1px solid #2a2f3a', backgroundColor: '#161616', padding: '0.75rem' },
  executionCard: { border: '1px solid #2a2f3a', borderLeft: '3px solid #0f62fe', backgroundColor: '#161616', padding: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  executionPrimary: { backgroundColor: '#0b0f17', borderLeftColor: '#78a9ff' },
  reviewCard: { border: '1px solid #393939', borderLeft: '3px solid #0f62fe', backgroundColor: '#161616', padding: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.45rem' },
  signalCard: { border: '1px solid #393939', borderLeft: '3px solid #33b1ff', backgroundColor: '#1f1f1f', padding: '0.6rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' },
  title: { margin: 0, color: '#f4f4f4', fontSize: '2rem', lineHeight: 1.15 },
  sectionHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '0.5rem' },
  sectionTitle: { margin: 0, color: '#f4f4f4', fontSize: '1rem', lineHeight: 1.25 },
  actionTitle: { margin: 0, color: '#f4f4f4', fontSize: '1.05rem', lineHeight: 1.25 },
  cardTitle: { color: '#f4f4f4', lineHeight: 1.25 },
  copy: { margin: 0, color: '#c6c6c6', lineHeight: 1.4, fontSize: '0.88rem' },
  meta: { margin: 0, color: '#8d8d8d', fontSize: '0.78rem', lineHeight: 1.35 },
  kicker: { margin: 0, color: '#78a9ff', textTransform: 'uppercase', fontSize: '0.72rem', letterSpacing: '0.06em' },
  rowBetween: { display: 'flex', justifyContent: 'space-between', gap: '0.75rem', alignItems: 'center' },
  tagRow: { display: 'flex', flexWrap: 'wrap', gap: '0.35rem' },
  tag: { border: '1px solid #393939', backgroundColor: '#262626', color: '#c6c6c6', padding: '0.15rem 0.4rem', fontSize: '0.72rem' },
  priorityTag: { border: '1px solid #0f62fe', backgroundColor: '#001d6c', color: '#78a9ff', padding: '0.15rem 0.4rem', fontSize: '0.72rem', fontWeight: 800 },
  countTag: { border: '1px solid #393939', color: '#c6c6c6', backgroundColor: '#262626', padding: '0.15rem 0.45rem', fontSize: '0.72rem' },
  buttonRow: { display: 'flex', gap: '0.45rem', flexWrap: 'wrap', alignItems: 'center' },
  primaryButton: { border: 'none', backgroundColor: '#0f62fe', color: '#fff', padding: '0.45rem 0.75rem', cursor: 'pointer', fontWeight: 700 },
  secondaryButton: { border: '1px solid #393939', backgroundColor: '#262626', color: '#f4f4f4', padding: '0.42rem 0.65rem', cursor: 'pointer', margin: '0.1rem' },
  linkButton: { border: 'none', background: 'transparent', color: '#78a9ff', padding: 0, cursor: 'pointer', textAlign: 'left' },
  link: { color: '#78a9ff' },
  details: { borderTop: '1px solid #262626', paddingTop: '0.45rem', color: '#c6c6c6', fontSize: '0.82rem' },
  summary: { color: '#f4f4f4', fontWeight: 700, cursor: 'pointer' },
  textarea: { width: '100%', boxSizing: 'border-box', minHeight: '4rem', marginTop: '0.5rem', border: '1px solid #393939', backgroundColor: '#0b0f17', color: '#f4f4f4', padding: '0.5rem' },
  cleanList: { listStyle: 'none', margin: 0, padding: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  listItem: { borderTop: '1px solid #262626', paddingTop: '0.5rem', color: '#c6c6c6', display: 'flex', flexDirection: 'column', gap: '0.15rem' },
  tableWrap: { overflow: 'auto', border: '1px solid #2a2f3a', backgroundColor: '#161616' },
  table: { width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' },
  th: { textAlign: 'left', color: '#8d8d8d', textTransform: 'uppercase', letterSpacing: '0.04em', borderBottom: '1px solid #393939', padding: '0.55rem', whiteSpace: 'nowrap' },
  td: { color: '#e0e0e0', borderBottom: '1px solid #262626', padding: '0.5rem', verticalAlign: 'top' },
}
