import { BrowserRouter, Routes, Route, Link, useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'

function Jobs() {
const [jobs, setJobs] = useState<any[]>([])

useEffect(() => {
fetch('/api/jobs')
.then((r) => r.json())
.then((d) => setJobs(d.items))
}, [])

return ( <div> <h1>Jobs</h1>
{jobs.map((j) => (
  <div key={j.id}>
    <Link to={`/jobs/${j.id}`}>{j.title}</Link>
  </div>
))} </div>
)
}

function JobDetail() {
const { jobId } = useParams()
return <h1>Job Detail {jobId}</h1>
}

export default function App() {
return ( <BrowserRouter> <Routes>
<Route path="/jobs" element={<Jobs />} />
<Route path="/jobs/:jobId" element={<JobDetail />} /> </Routes> </BrowserRouter>
)
}
