import type { CSSProperties } from 'react'
import { BrowserRouter, Navigate, Outlet, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import { GlobalShell } from './components/mvp/GlobalShell'
import {
  CompetitionPage,
  ComponentsPage,
  FoundationsPage,
  JobsPage,
  MessagesPage,
  OutreachPage,
  RecruitersPage,
  ReportsPage,
  ReviewQueuePage,
  SettingsPage,
  TodayPlanPage,
  WikiPage,
} from './features/mvp/MvpPages'
import { MvpStateProvider } from './state/mvpState'

const DEMO_AUTH_KEY = 'demo_auth'

function isAuthenticated() {
  return localStorage.getItem(DEMO_AUTH_KEY) === '1' || localStorage.getItem(DEMO_AUTH_KEY) === 'true'
}

function ProtectedRoute() {
  const location = useLocation()

  if (!isAuthenticated()) {
    return <Navigate to="/auth/sign-in" replace state={{ from: location }} />
  }

  return <Outlet />
}

function SignInPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname

  const handleSignIn = () => {
    localStorage.setItem(DEMO_AUTH_KEY, '1')
    navigate(from || '/review-queue', { replace: true })
  }

  return (
    <section style={styles.signInPage}>
      <div style={styles.signInCard}>
        <p style={styles.kicker}>JT7 v1.6</p>
        <h1 style={styles.title}>Sign in</h1>
        <p style={styles.copy}>Use demo auth to access the local MVP operator surface.</p>
        <button style={styles.primaryButton} onClick={handleSignIn} type="button">Sign in</button>
      </div>
    </section>
  )
}

function ShellRoute() {
  return (
    <MvpStateProvider>
      <GlobalShell />
    </MvpStateProvider>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/auth/sign-in" element={<SignInPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<ShellRoute />}>
            <Route path="/" element={<Navigate to="/review-queue" replace />} />
            <Route path="/review-queue" element={<ReviewQueuePage />} />
            <Route path="/execute/today" element={<TodayPlanPage />} />
            <Route path="/app/dashboard" element={<TodayPlanPage />} />
            <Route path="/jobs" element={<Navigate to="/manage/jobs" replace />} />
            <Route path="/manage/jobs" element={<JobsPage />} />
            <Route path="/manage/recruiters" element={<RecruitersPage />} />
            <Route path="/manage/outreach" element={<OutreachPage />} />
            <Route path="/manage/messages" element={<MessagesPage />} />
            <Route path="/intelligence/competition" element={<CompetitionPage />} />
            <Route path="/intelligence/wiki" element={<WikiPage />} />
            <Route path="/intelligence/reports" element={<ReportsPage />} />
            <Route path="/design-system/components" element={<ComponentsPage />} />
            <Route path="/design-system/foundations" element={<FoundationsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/review-queue" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

const styles: Record<string, CSSProperties> = {
  signInPage: {
    minHeight: '100vh',
    display: 'grid',
    placeItems: 'center',
    backgroundColor: '#0b0f17',
    color: '#f4f4f4',
    fontFamily: 'Inter, IBM Plex Sans, system-ui, sans-serif',
  },
  signInCard: {
    width: 'min(420px, calc(100vw - 2rem))',
    border: '1px solid #2a2f3a',
    borderTop: '3px solid #0f62fe',
    backgroundColor: '#161616',
    padding: '1rem',
  },
  kicker: {
    margin: 0,
    color: '#78a9ff',
    textTransform: 'uppercase',
    fontSize: '0.72rem',
    letterSpacing: '0.06em',
  },
  title: {
    margin: '0.25rem 0 0.5rem',
    fontSize: '2rem',
    color: '#f4f4f4',
  },
  copy: {
    margin: '0 0 1rem',
    color: '#c6c6c6',
  },
  primaryButton: {
    border: 'none',
    backgroundColor: '#0f62fe',
    color: '#fff',
    padding: '0.55rem 0.85rem',
    cursor: 'pointer',
    fontWeight: 700,
  },
}
