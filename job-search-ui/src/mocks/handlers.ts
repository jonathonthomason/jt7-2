import { http, HttpResponse } from 'msw'
import jobs from './fixtures/jobs.json'

export const handlers = [
http.get('/api/jobs', () => HttpResponse.json({ items: jobs })),
http.get('/api/jobs/:jobId', ({ params }) => {
return HttpResponse.json(jobs.find((j) => j.id === params.jobId))
}),
]
