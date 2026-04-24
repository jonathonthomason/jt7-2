import type { CSSProperties } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  BrowserRouter,
  Link,
  Navigate,
  Outlet,
  Route,
  Routes,
  useLocation,
  useNavigate,
  useParams,
} from 'react-router-dom'
import { TodayPlanPage } from './features/today'

const DEMO_AUTH_KEY = 'demo_auth'

type Job = {
  id: string
  title: string
  company: {
    name: string
    slug: string
  }
}

function isAuthenticated() {
  return localStorage.getItem(DEMO_AUTH_KEY) === '1'
}

async function fetchJobs(): Promise<{ items: Job[] }> {
  const response = await fetch('/api/jobs')
  if (!response.ok) throw new Error('Failed to fetch jobs')
  return response.json()
}

async function fetchJob(jobId: string): Promise<Job> {
  const response = await fetch(`/api/jobs/${jobId}`)
  if (!response.ok) throw new Error('Failed to fetch job')
  return response.json()
}

function AppShell() {
  return (
    <div style={styles.appShell}>
      <header style={styles.header}>
        <div style={styles.brand}>JT7 Job Search</div>
        <nav style={styles.nav}>
          <Link style={styles.link} to="/jobs">
            Jobs
          </Link>
          <Link style={styles.link} to="/app/dashboard">
            Dashboard
          </Link>
        </nav>
      </header>
      <main style={styles.main}>
        <Outlet />
      </main>
    </div>
  )
}

function ProtectedRoute() {
  const location = useLocation()

  if (!isAuthenticated()) {
    return <Navigate to="/auth/sign-in" replace state={{ from: location }} />
  }

  return <Outlet />
}

function JobsPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['jobs'],
    queryFn: fetchJobs,
  })

  if (isLoading) return <p style={styles.copy}>Loading jobs...</p>
  if (isError || !data) return <p style={styles.copy}>Unable to load jobs.</p>

  return (
    <section>
      <h1 style={styles.title}>Jobs</h1>
      <p style={styles.copy}>Browse active job opportunities sourced from mock API data.</p>
      <ul style={styles.cardList}>
        {data.items.map((job) => (
          <li key={job.id} style={styles.card}>
            <Link style={styles.cardTitleLink} to={`/jobs/${job.id}`}>
              {job.title}
            </Link>
            <div style={styles.metaRow}>
              <Link style={styles.link} to={`/companies/${job.company.slug}`}>
                {job.company.name}
              </Link>
            </div>
          </li>
        ))}
      </ul>
    </section>
  )
}

function JobDetailPage() {
  const { jobId = '' } = useParams()
  const { data, isLoading, isError } = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => fetchJob(jobId),
    enabled: Boolean(jobId),
  })

  if (isLoading) return <p style={styles.copy}>Loading job detail...</p>
  if (isError || !data) return <p style={styles.copy}>Unable to load job detail.</p>

  return (
    <section>
      <h1 style={styles.title}>{data.title}</h1>
      <p style={styles.copy}>Company: {data.company.name}</p>
      <p>
        <Link style={styles.link} to={`/companies/${data.company.slug}`}>
          Open company page
        </Link>
      </p>
    </section>
  )
}

function CompanyPage() {
  const { slug } = useParams()

  return (
    <section>
      <h1 style={styles.title}>Company</h1>
      <p style={styles.copy}>Company slug: {slug}</p>
    </section>
  )
}

function DashboardPage() {
  return <TodayPlanPage />
}

function SignInPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: { pathname?: string } } | null)?.from
    ?.pathname

  const handleSignIn = () => {
    localStorage.setItem(DEMO_AUTH_KEY, '1')
    navigate(from || '/app/dashboard', { replace: true })
  }

  return (
    <section>
      <h1 style={styles.title}>Sign In</h1>
      <p style={styles.copy}>Use demo auth to access protected areas.</p>
      <button style={styles.button} onClick={handleSignIn}>
        Sign in
      </button>
    </section>
  )
}

function NotFoundPage() {
  return <Navigate to="/jobs" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/jobs/:jobId" element={<JobDetailPage />} />
          <Route path="/companies/:slug" element={<CompanyPage />} />
          <Route path="/auth/sign-in" element={<SignInPage />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/app/dashboard" element={<DashboardPage />} />
          </Route>
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

const styles: Record<string, CSSProperties> = {
  appShell: {
    minHeight: '100vh',
    backgroundColor: '#0f172a',
    color: '#e2e8f0',
    fontFamily: 'Inter, system-ui, sans-serif',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1rem 1.5rem',
    borderBottom: '1px solid #1e293b',
    backgroundColor: '#111827',
  },
  brand: {
    fontSize: '1rem',
    fontWeight: 700,
  },
  nav: {
    display: 'flex',
    gap: '1rem',
  },
  link: {
    color: '#93c5fd',
    textDecoration: 'none',
  },
  main: {
    maxWidth: '960px',
    margin: '0 auto',
    padding: '2rem 1.5rem',
  },
  title: {
    margin: '0 0 0.75rem',
    fontSize: '2rem',
  },
  copy: {
    margin: '0 0 1rem',
    color: '#cbd5e1',
  },
  cardList: {
    display: 'grid',
    gap: '1rem',
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  card: {
    border: '1px solid #1e293b',
    backgroundColor: '#111827',
    borderRadius: '0.75rem',
    padding: '1rem',
  },
  cardTitleLink: {
    color: '#f8fafc',
    textDecoration: 'none',
    fontSize: '1.05rem',
    fontWeight: 600,
  },
  metaRow: {
    marginTop: '0.5rem',
  },
  button: {
    border: 'none',
    borderRadius: '0.5rem',
    padding: '0.7rem 1rem',
    backgroundColor: '#2563eb',
    color: '#fff',
    cursor: 'pointer',
  },
}
