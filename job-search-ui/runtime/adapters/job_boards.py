import json
import re
import subprocess
from html import unescape
from pathlib import Path
from urllib.parse import quote_plus


ROOT = Path('/Users/jtemp/.openclaw/workspace/job-search-ui')
INDEED_BROWSER_RESULTS = ROOT / 'runtime' / 'indeed_browser_results.json'


DEFAULT_CONFIG = {
    'builtin': {
        'enabled': True,
        'queries': [
            {'keywords': 'senior-product-designer', 'location_slug': 'remote', 'enabled': True},
            {'keywords': 'principal-product-designer', 'location_slug': 'remote', 'enabled': True},
            {'keywords': 'lead-product-designer', 'location_slug': 'remote', 'enabled': True},
            {'keywords': 'staff-product-designer', 'location_slug': 'remote', 'enabled': True},
            {'keywords': 'senior-product-designer', 'location_slug': 'dallas-fort-worth', 'enabled': True},
            {'keywords': 'principal-product-designer', 'location_slug': 'dallas-fort-worth', 'enabled': True},
            {'keywords': 'lead-product-designer', 'location_slug': 'dallas-fort-worth', 'enabled': True},
            {'keywords': 'staff-product-designer', 'location_slug': 'dallas-fort-worth', 'enabled': True},
        ],
    },
    'linkedin': {
        'enabled': True,
        'queries': [
            {'keywords': 'senior product designer', 'location': 'Dallas-Fort Worth Metroplex', 'enabled': True},
            {'keywords': 'staff product designer', 'location': 'Dallas-Fort Worth Metroplex', 'enabled': True},
            {'keywords': 'principal product designer', 'location': 'Dallas-Fort Worth Metroplex', 'enabled': True},
            {'keywords': 'product design manager', 'location': 'Dallas-Fort Worth Metroplex', 'enabled': True},
            {'keywords': 'lead product designer', 'location': 'Dallas-Fort Worth Metroplex', 'enabled': True},
            {'keywords': 'product designer', 'location': 'Remote', 'enabled': True},
        ],
    },
    'indeed': {
        'enabled': True,
        'queries': [
            {'keywords': 'senior product designer', 'location': 'Remote', 'enabled': True},
            {'keywords': 'senior product designer', 'location': 'Dallas-Fort Worth, TX', 'enabled': True},
        ],
    },
    'greenhouse': {
        'enabled': True,
        'boards': [
            {'token': 'webflow', 'company': 'Webflow', 'enabled': True},
            {'token': 'coinbase', 'company': 'Coinbase', 'enabled': True},
            {'token': 'robinhood', 'company': 'Robinhood', 'enabled': True},
            {'token': 'affirm', 'company': 'Affirm', 'enabled': True},
            {'token': 'duolingo', 'company': 'Duolingo', 'enabled': True},
            {'token': 'dropbox', 'company': 'Dropbox', 'enabled': True},
            {'token': 'stripe', 'company': 'Stripe', 'enabled': True},
        ],
    },
    'filters': {
        'allowed_location_keywords': [
            'remote',
            'dallas',
            'fort worth',
            'dfw',
            'dallas-fort worth',
            'dallas fort worth',
            'irving',
            'plano',
            'frisco',
            'addison',
            'grapevine',
            'arlington',
            'richardson'
        ],
        'include_title_keywords': [
            'product designer',
            'senior product designer',
            'principal product designer',
            'lead product designer',
            'staff product designer',
            'ux designer',
            'user experience designer',
            'product design manager',
            'design lead',
            'founding product designer',
        ],
        'exclude_title_keywords': [
            'brand designer',
            'design program manager',
            'executive assistant',
            'design technologist',
            'content designer',
            'data center design',
            'onsite',
            'on-site',
        ],
    },
}


def ensure_job_board_targets(path: Path):
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(DEFAULT_CONFIG, indent=2))


def load_job_board_targets(path: Path):
    ensure_job_board_targets(path)
    return json.loads(path.read_text())


def fetch_text(url: str, timeout_seconds: int = 15):
    return subprocess.check_output(
        ['curl', '-L', '--silent', '--show-error', '--max-time', str(timeout_seconds), '-A', 'Mozilla/5.0', url],
        text=True,
    )


def fetch_json(url: str, timeout_seconds: int = 15):
    raw = fetch_text(url, timeout_seconds=timeout_seconds)
    return json.loads(raw)


def greenhouse_jobs(board_token: str):
    payload = fetch_json(f'https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs')
    return payload.get('jobs', [])


def title_matches(job_title: str, include_keywords: list[str], exclude_keywords: list[str]):
    title = (job_title or '').strip().lower()
    if not title:
        return False
    if any(keyword in title for keyword in exclude_keywords):
        return False
    return any(keyword in title for keyword in include_keywords)


def location_matches(location: str, allowed_keywords: list[str]):
    loc = (location or '').strip().lower()
    if not loc:
        return False
    return any(keyword in loc for keyword in allowed_keywords)


def job_matches_location_constraints(role: str, location: str, search_location: str, allowed_keywords: list[str]):
    role_norm = (role or '').strip().lower()
    location_norm = (location or '').strip().lower()
    search_location_norm = (search_location or '').strip().lower()
    if 'remote' in role_norm or 'remote' in location_norm:
        return True
    if search_location_norm == 'remote':
        return True
    return location_matches(location, allowed_keywords)


def normalize_greenhouse_job(job: dict, board: dict):
    return {
        'source': 'greenhouse',
        'board_token': board.get('token', ''),
        'company': job.get('company_name') or board.get('company') or board.get('token', ''),
        'role': job.get('title', ''),
        'location': (job.get('location') or {}).get('name', ''),
        'job_posting_link': job.get('absolute_url', ''),
        'job_board_id': str(job.get('id', '')),
        'first_published': job.get('first_published', ''),
        'updated_at': job.get('updated_at', ''),
    }


def clean_html_text(value: str):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', unescape(value or ''))).strip()


def parse_builtin_listings(html: str, query: dict):
    itemlist_match = re.search(r'\{"@type":"ItemList","name":"Top .*? Jobs","numberOfItems":\d+,"itemListElement":\[(.*?)\]\}', html, re.S)
    if not itemlist_match:
        return []
    rows = []
    for name, url in re.findall(r'"name":"(.*?)","url":"(https://builtin\.com/job/[^"]+)"', itemlist_match.group(1)):
        rows.append({
            'source': 'builtin',
            'board_token': query.get('location_slug', ''),
            'company': '',
            'role': clean_html_text(name),
            'location': 'Remote' if query.get('location_slug') == 'remote' else 'Dallas-Fort Worth, TX',
            'job_posting_link': clean_html_text(url),
            'job_board_id': clean_html_text(url).rstrip('/').split('/')[-1],
            'first_published': '',
            'updated_at': '',
            'search_keywords': query.get('keywords', ''),
            'search_location': query.get('location_slug', ''),
        })
    deduped = []
    seen = set()
    for row in rows:
        key = row['job_posting_link']
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def enrich_builtin_job(match: dict):
    try:
        html = fetch_text(match['job_posting_link'], timeout_seconds=20)
    except subprocess.CalledProcessError:
        return match
    title_match = re.search(r'<title>(.*?)</title>', html, re.S)
    company_match = re.search(r'"hiringOrganization":\{"@type":"Organization","name":"(.*?)"', html, re.S)
    remote_match = re.search(r'"jobLocationType":"(.*?)"', html, re.S)
    location_match = re.search(r'"jobLocation":\[(.*?)\]', html, re.S)
    role = match.get('role', '')
    if title_match:
        title_text = clean_html_text(title_match.group(1).replace('| Built In', ''))
        if ' - ' in title_text:
            role = title_text.split(' - ')[0].strip()
        else:
            role = title_text.strip()
    location = match.get('location', '')
    if remote_match and remote_match.group(1) == 'TELECOMMUTE':
        location = 'Remote'
    elif location_match:
        localities = re.findall(r'"addressLocality":"(.*?)"', location_match.group(1))
        regions = re.findall(r'"addressRegion":"(.*?)"', location_match.group(1))
        if localities:
            locs = []
            for i, city in enumerate(localities):
                region = regions[i] if i < len(regions) else ''
                locs.append(f"{city}, {region}".strip(', '))
            location = ' | '.join(dict.fromkeys(locs))
    return {
        **match,
        'company': clean_html_text(company_match.group(1)) if company_match else match.get('company', ''),
        'role': role,
        'location': location,
    }


def parse_linkedin_cards(html: str, query: dict):
    rows = []
    blocks = html.split('<li>')
    for block in blocks:
        if 'base-search-card__title' not in block:
            continue
        link_match = re.search(r'href="(https://www\.linkedin\.com/jobs/view/[^"]+)"', block)
        title_match = re.search(r'<h3 class="base-search-card__title">([\s\S]*?)</h3>', block)
        company_match = re.search(r'<h4 class="base-search-card__subtitle">([\s\S]*?)</h4>', block)
        location_match = re.search(r'<span class="job-search-card__location">([\s\S]*?)</span>', block)
        if not (link_match and title_match and company_match and location_match):
            continue
        link = unescape(link_match.group(1))
        title = title_match.group(1)
        company = company_match.group(1)
        location = location_match.group(1)
        rows.append({
            'source': 'linkedin',
            'board_token': 'linkedin_guest',
            'company': clean_html_text(company),
            'role': clean_html_text(title),
            'location': clean_html_text(location),
            'job_posting_link': link,
            'job_board_id': link.split('?')[0].rstrip('/').split('-')[-1],
            'first_published': '',
            'updated_at': '',
            'search_keywords': query.get('keywords', ''),
            'search_location': query.get('location', ''),
        })
    deduped = []
    seen = set()
    for row in rows:
        key = row['job_posting_link']
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def scan_builtin_targets(config: dict):
    builtin = config.get('builtin', {})
    filters = config.get('filters', {})
    queries = [query for query in builtin.get('queries', []) if query.get('enabled', True)]
    include_keywords = [value.lower() for value in filters.get('include_title_keywords', [])]
    exclude_keywords = [value.lower() for value in filters.get('exclude_title_keywords', [])]
    allowed_location_keywords = [value.lower() for value in filters.get('allowed_location_keywords', [])]
    matches = []
    reports = []
    warnings = []
    for query in queries:
        keywords = query.get('keywords', '').strip()
        location_slug = query.get('location_slug', '').strip()
        url = f"https://builtin.com/jobs/{location_slug}/design-ux/search/{keywords}"
        try:
            html = fetch_text(url)
            jobs = [
                enrich_builtin_job(row)
                for row in parse_builtin_listings(html, query)
                if title_matches(row.get('role', ''), include_keywords, exclude_keywords)
                and job_matches_location_constraints(row.get('role', ''), row.get('location', ''), 'Remote' if location_slug == 'remote' else 'Dallas-Fort Worth Metroplex', allowed_location_keywords)
            ]
            matches.extend(jobs)
            reports.append({'source': 'builtin', 'query': keywords, 'location': location_slug, 'status': 'complete', 'matches': len(jobs)})
        except subprocess.CalledProcessError as exc:
            warnings.append(f'builtin:{keywords}:{location_slug} fetch failed ({exc.returncode})')
            reports.append({'source': 'builtin', 'query': keywords, 'location': location_slug, 'status': 'failed', 'matches': 0})
    deduped = []
    seen = set()
    for row in matches:
        key = row['job_posting_link']
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped, reports, warnings


def scan_linkedin_targets(config: dict):
    linkedin = config.get('linkedin', {})
    filters = config.get('filters', {})
    queries = [query for query in linkedin.get('queries', []) if query.get('enabled', True)]
    include_keywords = [value.lower() for value in filters.get('include_title_keywords', [])]
    exclude_keywords = [value.lower() for value in filters.get('exclude_title_keywords', [])]
    allowed_location_keywords = [value.lower() for value in filters.get('allowed_location_keywords', [])]
    matches = []
    reports = []
    warnings = []
    for query in queries:
        keywords = query.get('keywords', '').strip()
        location = query.get('location', '').strip()
        url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(keywords)}&location={quote_plus(location)}"
        try:
            html = fetch_text(url)
            jobs = [
                row for row in parse_linkedin_cards(html, query)
                if title_matches(row.get('role', ''), include_keywords, exclude_keywords)
                and job_matches_location_constraints(row.get('role', ''), row.get('location', ''), query.get('location', ''), allowed_location_keywords)
            ]
            matches.extend(jobs)
            reports.append({'source': 'linkedin', 'query': keywords, 'location': location, 'status': 'complete', 'matches': len(jobs)})
        except subprocess.CalledProcessError as exc:
            warnings.append(f'linkedin:{keywords}:{location} fetch failed ({exc.returncode})')
            reports.append({'source': 'linkedin', 'query': keywords, 'location': location, 'status': 'failed', 'matches': 0})
    deduped = []
    seen = set()
    for row in matches:
        key = row['job_posting_link']
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped, reports, warnings


def scan_indeed_targets(config: dict):
    indeed = config.get('indeed', {})
    queries = [query for query in indeed.get('queries', []) if query.get('enabled', True)]
    reports = []
    warnings = []

    browser_scan_cmd = ['node', str(ROOT / 'scripts' / 'indeed_browser_scan.cjs'), 'scan']
    try:
        raw = subprocess.check_output(browser_scan_cmd, text=True)
        payload = json.loads(raw)
        jobs = payload.get('jobs', [])
        report_index = {(row.get('query', ''), row.get('location', '')): row for row in payload.get('reports', [])}
        for query in queries:
            key = (query.get('keywords', '').strip(), query.get('location', '').strip())
            report = report_index.get(key, {'source': 'indeed', 'query': key[0], 'location': key[1], 'status': 'failed', 'matches': 0})
            reports.append(report)
        warnings.extend(payload.get('warnings', []))
        return jobs, reports, warnings
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        for query in queries:
            keywords = query.get('keywords', '').strip()
            location = query.get('location', '').strip()
            warnings.append(f'indeed:{keywords}:{location} blocked - run node scripts/indeed_browser_scan.cjs setup')
            reports.append({'source': 'indeed', 'query': keywords, 'location': location, 'status': 'blocked', 'matches': 0})
        return [], reports, warnings


def scan_greenhouse_targets(config: dict):
    greenhouse = config.get('greenhouse', {})
    filters = config.get('filters', {})
    boards = [board for board in greenhouse.get('boards', []) if board.get('enabled', True)]
    include_keywords = [value.lower() for value in filters.get('include_title_keywords', [])]
    exclude_keywords = [value.lower() for value in filters.get('exclude_title_keywords', [])]
    allowed_location_keywords = [value.lower() for value in filters.get('allowed_location_keywords', [])]

    matches = []
    board_reports = []
    warnings = []

    for board in boards:
        token = board.get('token', '').strip()
        if not token:
            continue
        try:
            jobs = greenhouse_jobs(token)
        except subprocess.CalledProcessError as exc:
            warnings.append(f'greenhouse:{token} fetch failed ({exc.returncode})')
            board_reports.append({
                'source': 'greenhouse',
                'board_token': token,
                'company': board.get('company', token),
                'status': 'failed',
                'jobs_seen': 0,
                'matches': 0,
            })
            continue
        except json.JSONDecodeError:
            warnings.append(f'greenhouse:{token} returned invalid json')
            board_reports.append({
                'source': 'greenhouse',
                'board_token': token,
                'company': board.get('company', token),
                'status': 'failed',
                'jobs_seen': 0,
                'matches': 0,
            })
            continue

        board_matches = [
            normalize_greenhouse_job(job, board)
            for job in jobs
            if title_matches(job.get('title', ''), include_keywords, exclude_keywords)
            and job_matches_location_constraints(job.get('title', ''), (job.get('location') or {}).get('name', ''), '', allowed_location_keywords)
        ]
        matches.extend(board_matches)
        board_reports.append({
            'source': 'greenhouse',
            'board_token': token,
            'company': board.get('company', token),
            'status': 'complete',
            'jobs_seen': len(jobs),
            'matches': len(board_matches),
        })

    matches.sort(key=lambda row: (row.get('company', ''), row.get('role', '')))
    return matches, board_reports, warnings
