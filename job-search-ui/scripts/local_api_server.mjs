import { createServer } from 'node:http'
import { spawn } from 'node:child_process'
import { URL } from 'node:url'

const HOST = process.env.HOST || '127.0.0.1'
const PORT = Number(process.env.PORT || 8787)
const WORKDIR = '/Users/jtemp/.openclaw/workspace'
const APPLY_SCRIPT = '/Users/jtemp/.openclaw/workspace/job-search-ui/scripts/apply_staging_writeback.py'

function json(res, status, payload) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
  })
  res.end(JSON.stringify(payload))
}

function collectBody(req) {
  return new Promise((resolve, reject) => {
    let body = ''
    req.on('data', (chunk) => { body += chunk })
    req.on('end', () => resolve(body))
    req.on('error', reject)
  })
}

function runWriteback({ stagedId, apply }) {
  return new Promise((resolve, reject) => {
    const args = [APPLY_SCRIPT, '--staged-id', stagedId, '--json']
    if (apply) args.splice(3, 0, '--apply')
    const child = spawn('python3', args, { cwd: WORKDIR })
    let stdout = ''
    let stderr = ''

    child.stdout.on('data', (chunk) => { stdout += chunk.toString() })
    child.stderr.on('data', (chunk) => { stderr += chunk.toString() })
    child.on('error', reject)
    child.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(stderr.trim() || stdout.trim() || `writeback exited ${code}`))
        return
      }
      try {
        resolve(JSON.parse(stdout))
      } catch (error) {
        reject(new Error(`Invalid JSON from writeback script: ${stdout}`))
      }
    })
  })
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url || '/', `http://${HOST}:${PORT}`)

  if (req.method === 'OPTIONS') {
    json(res, 204, {})
    return
  }

  if (req.method === 'GET' && url.pathname === '/api/health') {
    json(res, 200, { ok: true, service: 'jt7-local-api' })
    return
  }

  if (req.method === 'POST' && url.pathname === '/api/staging/writeback') {
    try {
      const raw = await collectBody(req)
      const body = raw ? JSON.parse(raw) : {}
      const stagedId = typeof body.stagedId === 'string' ? body.stagedId : ''
      const command = typeof body.command === 'string' ? body.command : ''
      const apply = Boolean(body.apply)

      if (!stagedId) {
        json(res, 400, { error: 'stagedId is required' })
        return
      }
      if (command !== 'Promote' && command !== 'Merge') {
        json(res, 400, { error: 'Only Promote or Merge are supported by the runtime writeback API' })
        return
      }

      const payload = await runWriteback({ stagedId, apply })
      json(res, 200, payload)
      return
    } catch (error) {
      json(res, 500, { error: error instanceof Error ? error.message : 'Unknown writeback error' })
      return
    }
  }

  json(res, 404, { error: 'Not found' })
})

server.listen(PORT, HOST, () => {
  console.log(`JT7 local API listening on http://${HOST}:${PORT}`)
})
