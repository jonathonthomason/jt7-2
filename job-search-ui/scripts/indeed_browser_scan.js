#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { chromium } = require('../node_modules/playwright');

const ROOT = '/Users/jtemp/.openclaw/workspace/job-search-ui';
const RUNTIME = path.join(ROOT, 'runtime');
const TARGETS_PATH = path.join(RUNTIME, 'job_board_targets.json');
const PROFILE_DIR = path.join(RUNTIME, 'browser_profiles', 'indeed');
const OUTPUT_PATH = path.join(RUNTIME, 'indeed_browser_results.json');

function loadTargets() {
  return JSON.parse(fs.readFileSync(TARGETS_PATH, 'utf8'));
}

function indeedQueries() {
  const config = loadTargets();
  return (config.indeed?.queries || []).filter(q => q.enabled !== false);
}

function searchUrl(query) {
  const params = new URLSearchParams({ q: query.keywords || '', l: query.location || '' });
  return `https://www.indeed.com/jobs?${params.toString()}`;
}

function looksBlocked(title, bodyText) {
  const t = (title || '').toLowerCase();
  const b = (bodyText || '').toLowerCase();
  return t.includes('blocked') || t.includes('security check') || b.includes('security check') || b.includes('verify you are a human') || b.includes('additional verification required');
}

async function scrapePage(page, query) {
  await page.waitForTimeout(2500);
  const title = await page.title();
  const bodyText = await page.locator('body').innerText().catch(() => '');
  if (looksBlocked(title, bodyText)) {
    return { blocked: true, title, jobs: [] };
  }

  const jobs = await page.evaluate((query) => {
    const clean = (v) => (v || '').replace(/\s+/g, ' ').trim();
    const cards = Array.from(document.querySelectorAll('a[href*="/rc/clk"], a[href*="/pagead/clk"], a[href*="/viewjob"]'));
    const seen = new Set();
    const rows = [];
    for (const card of cards) {
      const href = card.href;
      if (!href || seen.has(href)) continue;
      const container = card.closest('[data-jk], .job_seen_beacon, .slider_item, .result, li, div') || card;
      const text = clean(container.innerText || '');
      if (!text) continue;
      const role = clean(card.textContent || container.querySelector('h2,h3')?.textContent || '');
      const company = clean(container.querySelector('[data-testid="company-name"], .companyName, [data-company-name="true"]')?.textContent || '');
      const location = clean(container.querySelector('[data-testid="text-location"], .companyLocation')?.textContent || '');
      if (!role) continue;
      seen.add(href);
      rows.push({
        source: 'indeed',
        board_token: 'indeed_browser',
        company,
        role,
        location,
        job_posting_link: href,
        job_board_id: href,
        first_published: '',
        updated_at: '',
        search_keywords: query.keywords || '',
        search_location: query.location || '',
        raw_text: text.slice(0, 400),
      });
    }
    return rows;
  }, query);

  return { blocked: false, title, jobs };
}

async function runSetup() {
  fs.mkdirSync(PROFILE_DIR, { recursive: true });
  const queries = indeedQueries();
  const url = searchUrl(queries[0] || { keywords: 'senior product designer', location: 'Remote' });
  const context = await chromium.launchPersistentContext(PROFILE_DIR, { headless: false });
  const page = context.pages()[0] || await context.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  console.log('\nIndeed setup window opened.');
  console.log('If a security check or login appears, complete it in the browser window.');
  console.log('When the Indeed jobs page is usable, press Enter here to save the session.\n');
  process.stdin.resume();
  await new Promise(resolve => process.stdin.once('data', resolve));
  await context.close();
  console.log('Indeed browser profile saved to:', PROFILE_DIR);
}

async function runScan() {
  fs.mkdirSync(PROFILE_DIR, { recursive: true });
  const queries = indeedQueries();
  const context = await chromium.launchPersistentContext(PROFILE_DIR, { headless: true });
  const results = [];
  const warnings = [];
  for (const query of queries) {
    const page = await context.newPage();
    const url = searchUrl(query);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const { blocked, title, jobs } = await scrapePage(page, query);
    results.push({ source: 'indeed', query: query.keywords, location: query.location, status: blocked ? 'blocked' : 'complete', matches: jobs.length, title });
    if (blocked) warnings.push(`indeed:${query.keywords}:${query.location} blocked - run setup`);
    for (const job of jobs) results.push(job);
    await page.close();
  }
  await context.close();

  const payload = {
    generated_at: new Date().toISOString(),
    reports: results.filter(r => r.source === 'indeed' && Object.prototype.hasOwnProperty.call(r, 'status')),
    jobs: results.filter(r => r.source === 'indeed' && Object.prototype.hasOwnProperty.call(r, 'job_posting_link')),
    warnings,
  };
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(payload, null, 2));
  console.log(JSON.stringify(payload, null, 2));
}

(async () => {
  const mode = process.argv[2] || 'scan';
  if (mode === 'setup') return runSetup();
  if (mode === 'scan') return runScan();
  console.error('Usage: indeed_browser_scan.js [setup|scan]');
  process.exit(1);
})().catch(err => {
  console.error(err);
  process.exit(1);
});
