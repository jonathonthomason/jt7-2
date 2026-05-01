import type { CSSProperties, ReactNode } from 'react'
import type { MvpAction, MvpJob, MvpMessage, MvpRecruiter, MvpSignal } from '../../state/mvpState'
import type { ReviewItem, StagedOpportunity } from '../../domain/cockpit/types'
import { NavLink, Outlet } from 'react-router-dom'
import { useMvpState } from '../../state/mvpState'

type NavGroup = { label: string; items: { label: string; to: string }[] }

const navGroups: NavGroup[] = [
  { label: 'Trust', items: [{ label: 'Review Queue', to: '/review-queue' }, { label: 'Staging Intake', to: '/trust/staging' }] },
  { label: 'Execute', items: [{ label: 'Today', to: '/execute/today' }] },
  {
    label: 'Manage',
    items: [
      { label: 'Jobs', to: '/manage/jobs' },
      { label: 'Recruiters', to: '/manage/recruiters' },
      { label: 'Outreach', to: '/manage/outreach' },
      { label: 'Messages', to: '/manage/messages' },
    ],
  },
  {
    label: 'Intelligence',
    items: [
      { label: 'Competition', to: '/intelligence/competition' },
      { label: 'Wiki', to: '/intelligence/wiki' },
      { label: 'Reports', to: '/intelligence/reports' },
    ],
  },
  {
    label: 'System',
    items: [
      { label: 'Components', to: '/design-system/components' },
      { label: 'Foundations', to: '/design-system/foundations' },
      { label: 'Settings', to: '/settings' },
    ],
  },
]

function PanelBody() {
  const { state, closePanel, updatePanelNote, actionCommand, jobCommand, recruiterCommand, reviewCommand, stagingCommand } = useMvpState()
  const { type, id } = state.selectedPanel
  if (!type || !id) return <p style={styles.panelEmpty}>Open a review item, signal, job, recruiter, action, or message.</p>

  const object: MvpSignal | MvpJob | MvpRecruiter | MvpAction | MvpMessage | ReviewItem | StagedOpportunity | undefined = type === 'review'
    ? state.reviewQueue.find((item) => item.id === id)
    : type === 'staging'
      ? state.stagingQueue.find((item) => item.id === id)
      : type === 'signal'
        ? state.signals.find((item) => item.id === id)
        : type === 'job'
          ? state.jobs.find((item) => item.id === id)
          : type === 'recruiter'
            ? state.recruiters.find((item) => item.id === id)
            : type === 'action'
              ? state.actions.find((item) => item.id === id)
              : state.messages.find((item) => item.id === id)

  if (!object) return <p style={styles.panelEmpty}>Object not found.</p>

  const panelRecord = object as Record<string, string | undefined>
  const title = panelRecord.title || panelRecord.extractedRole || panelRecord.role || panelRecord.name || panelRecord.subject || panelRecord.summary || panelRecord.extractedCompany || 'Detail'
  const status = panelRecord.status || 'unknown'
  const source = panelRecord.source || panelRecord.channel || 'local state'
  const summary = panelRecord.summary || panelRecord.evidenceSummary || panelRecord.whyNow || panelRecord.nextAction || panelRecord.recommendedAction || panelRecord.reasonForReview || ''
  const notes = panelRecord.notes || panelRecord.note || panelRecord.resolutionNotes || ''
  const related = panelRecord.company || panelRecord.extractedCompany || panelRecord.target || 'JT7'

  return (
    <div style={styles.panelStack}>
      <div style={styles.panelHeaderRow}>
        <div>
          <p style={styles.kicker}>{type}</p>
          <h2 style={styles.panelTitle}>{title}</h2>
        </div>
        <button style={styles.iconButton} onClick={closePanel} type="button">×</button>
      </div>
      <div style={styles.tagRow}>
        <span style={styles.tag}>{status}</span>
        <span style={styles.tag}>{source}</span>
      </div>
      <p style={styles.panelCopy}>{summary}</p>
      <div>
        <p style={styles.kicker}>Related</p>
        <p style={styles.panelCopy}>{related}</p>
      </div>
      <label style={styles.noteLabel}>
        Note / status detail
        <textarea style={styles.noteArea} value={notes} onChange={(event) => updatePanelNote(event.target.value)} placeholder="Add operator note…" />
      </label>
      <div style={styles.panelActions}>
        {type === 'review' ? (
          <>
            <button style={styles.primaryButton} onClick={() => reviewCommand(id, 'Confirm')} type="button">Confirm</button>
            <button style={styles.secondaryButton} onClick={() => reviewCommand(id, 'Link')} type="button">Link</button>
            <button style={styles.secondaryButton} onClick={() => reviewCommand(id, 'Dismiss')} type="button">Dismiss</button>
            <button style={styles.secondaryButton} onClick={() => reviewCommand(id, 'Escalate')} type="button">Escalate</button>
          </>
        ) : null}
        {type === 'staging' ? (
          <>
            {'duplicateMatches' in object && Array.isArray(object.duplicateMatches) && object.duplicateMatches.length ? <button style={styles.primaryButton} onClick={() => stagingCommand(id, 'Merge')} type="button">Merge</button> : <button style={styles.primaryButton} onClick={() => stagingCommand(id, 'Promote')} type="button">Promote</button>}
            <button style={styles.secondaryButton} onClick={() => stagingCommand(id, 'Hold')} type="button">Hold</button>
            <button style={styles.secondaryButton} onClick={() => stagingCommand(id, 'Reject')} type="button">Reject</button>
          </>
        ) : null}
        {type === 'action' ? <button style={styles.primaryButton} onClick={() => actionCommand(id, 'Complete')} type="button">Complete</button> : null}
        {type === 'job' ? <button style={styles.primaryButton} onClick={() => jobCommand(id, 'Review')} type="button">Review</button> : null}
        {type === 'recruiter' ? <button style={styles.primaryButton} onClick={() => recruiterCommand(id, 'Draft Reply')} type="button">Draft Reply</button> : null}
        <button style={styles.secondaryButton} onClick={closePanel} type="button">Close</button>
      </div>
    </div>
  )
}

export function GlobalShell({ children }: { children?: ReactNode }) {
  const { state, today, reviewSummary, runSweep, refreshPlan } = useMvpState()

  return (
    <div style={styles.shell}>
      <aside style={styles.sideNav}>
        <div style={styles.brand}>JT7</div>
        {navGroups.map((group) => (
          <nav key={group.label} style={styles.navGroup} aria-label={group.label}>
            <p style={styles.navGroupLabel}>{group.label}</p>
            {group.items.map((item) => (
              <NavLink key={item.to} to={item.to} style={({ isActive }) => ({ ...styles.navLink, ...(isActive ? styles.navLinkActive : {}) })}>
                {item.label}
              </NavLink>
            ))}
          </nav>
        ))}
      </aside>
      <div style={styles.mainRegion}>
        <header style={styles.header}>
          <div style={styles.contextSwitcher}>JT Personal / <strong>Job Search</strong></div>
          <input style={styles.commandInput} placeholder="Command or search…" onKeyDown={(event) => {
            if (event.key === 'Enter' && event.currentTarget.value.toLowerCase().includes('sweep')) runSweep()
          }} />
          <div style={styles.headerActions}>
            <button style={styles.secondaryButton} onClick={refreshPlan} type="button">Refresh</button>
            <button style={styles.primaryButton} onClick={runSweep} type="button">Run Sweep</button>
            <span style={styles.signalTray}>{reviewSummary.pending.length} pending reviews</span>
            <span style={styles.signalTray}>{today.newSignals.length} signals</span>
          </div>
        </header>
        <main style={styles.content}>{children ?? <Outlet />}</main>
      </div>
      <aside style={styles.rightPanel}>
        <div style={styles.panelTopMeta}>Last updated {state.lastUpdated}</div>
        <PanelBody />
      </aside>
    </div>
  )
}

const styles: Record<string, CSSProperties> = {
  shell: {
    minHeight: '100vh',
    display: 'grid',
    gridTemplateColumns: '240px minmax(0, 1fr) 320px',
    backgroundColor: '#0b0f17',
    color: '#f4f4f4',
    fontFamily: 'Inter, IBM Plex Sans, system-ui, sans-serif',
    textAlign: 'left',
  },
  sideNav: {
    borderRight: '1px solid #262626',
    backgroundColor: '#161616',
    padding: '1rem 0.75rem',
  },
  brand: {
    fontSize: '1.25rem',
    fontWeight: 800,
    letterSpacing: '0.08em',
    marginBottom: '1rem',
  },
  navGroup: { marginBottom: '1rem' },
  navGroupLabel: {
    margin: '0 0 0.35rem',
    color: '#8d8d8d',
    textTransform: 'uppercase',
    fontSize: '0.72rem',
    letterSpacing: '0.08em',
  },
  navLink: {
    display: 'block',
    color: '#c6c6c6',
    textDecoration: 'none',
    padding: '0.45rem 0.5rem',
    borderLeft: '3px solid transparent',
    fontSize: '0.9rem',
  },
  navLinkActive: {
    color: '#ffffff',
    backgroundColor: '#262626',
    borderLeftColor: '#0f62fe',
  },
  mainRegion: { minWidth: 0, display: 'flex', flexDirection: 'column' },
  header: {
    minHeight: '56px',
    borderBottom: '1px solid #262626',
    backgroundColor: '#161616',
    display: 'grid',
    gridTemplateColumns: '180px minmax(220px, 1fr) auto',
    gap: '0.75rem',
    alignItems: 'center',
    padding: '0.5rem 1rem',
  },
  contextSwitcher: { color: '#c6c6c6', fontSize: '0.85rem' },
  commandInput: {
    width: '100%',
    boxSizing: 'border-box',
    border: '1px solid #393939',
    backgroundColor: '#0b0f17',
    color: '#f4f4f4',
    padding: '0.45rem 0.65rem',
  },
  headerActions: { display: 'flex', gap: '0.5rem', alignItems: 'center', flexWrap: 'wrap' },
  content: { padding: '1rem', overflow: 'auto' },
  rightPanel: {
    borderLeft: '1px solid #262626',
    backgroundColor: '#161616',
    padding: '0.75rem',
    overflow: 'auto',
  },
  panelTopMeta: { color: '#8d8d8d', fontSize: '0.72rem', marginBottom: '0.75rem' },
  panelEmpty: { color: '#8d8d8d', margin: 0, lineHeight: 1.4 },
  panelStack: { display: 'flex', flexDirection: 'column', gap: '0.75rem' },
  panelHeaderRow: { display: 'flex', justifyContent: 'space-between', gap: '0.75rem' },
  panelTitle: { margin: '0.15rem 0 0', fontSize: '1.1rem', lineHeight: 1.25, color: '#f4f4f4' },
  panelCopy: { margin: 0, color: '#c6c6c6', lineHeight: 1.45, fontSize: '0.88rem' },
  kicker: { margin: 0, color: '#78a9ff', textTransform: 'uppercase', fontSize: '0.72rem', letterSpacing: '0.06em' },
  tagRow: { display: 'flex', flexWrap: 'wrap', gap: '0.4rem' },
  tag: { border: '1px solid #393939', backgroundColor: '#262626', color: '#c6c6c6', padding: '0.15rem 0.45rem', fontSize: '0.72rem' },
  noteLabel: { display: 'flex', flexDirection: 'column', gap: '0.35rem', color: '#c6c6c6', fontSize: '0.8rem' },
  noteArea: { minHeight: '6rem', border: '1px solid #393939', backgroundColor: '#0b0f17', color: '#f4f4f4', padding: '0.5rem' },
  panelActions: { display: 'flex', gap: '0.5rem', flexWrap: 'wrap' },
  primaryButton: { border: 'none', backgroundColor: '#0f62fe', color: '#fff', padding: '0.45rem 0.75rem', cursor: 'pointer', fontWeight: 700 },
  secondaryButton: { border: '1px solid #393939', backgroundColor: '#262626', color: '#f4f4f4', padding: '0.45rem 0.75rem', cursor: 'pointer' },
  iconButton: { border: '1px solid #393939', backgroundColor: '#262626', color: '#f4f4f4', cursor: 'pointer', height: '2rem', width: '2rem' },
  signalTray: { border: '1px solid #393939', backgroundColor: '#262626', color: '#33b1ff', padding: '0.35rem 0.6rem', fontSize: '0.78rem' },
}
