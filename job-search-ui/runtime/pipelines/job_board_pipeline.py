from pathlib import Path

from runtime.adapters.job_boards import load_job_board_targets, scan_builtin_targets, scan_greenhouse_targets, scan_indeed_targets, scan_linkedin_targets


ROOT = Path('/Users/jtemp/.openclaw/workspace/job-search-ui')
TARGETS = ROOT / 'runtime' / 'job_board_targets.json'


def job_board_scan_report():
    config = load_job_board_targets(TARGETS)
    builtin_matches, builtin_reports, builtin_warnings = scan_builtin_targets(config)
    linkedin_matches, linkedin_reports, linkedin_warnings = scan_linkedin_targets(config)
    indeed_matches, indeed_reports, indeed_warnings = scan_indeed_targets(config)
    greenhouse_matches, greenhouse_reports, greenhouse_warnings = scan_greenhouse_targets(config)

    all_matches = builtin_matches + linkedin_matches + indeed_matches + greenhouse_matches
    all_reports = builtin_reports + linkedin_reports + indeed_reports + greenhouse_reports
    successful = []
    for row in builtin_reports:
        if row.get('status') == 'complete':
            successful.append(f"builtin:{row['query']}:{row['location']}")
    for row in linkedin_reports:
        if row.get('status') == 'complete':
            successful.append(f"linkedin:{row['query']}:{row['location']}")
    for row in indeed_reports:
        if row.get('status') == 'complete':
            successful.append(f"indeed:{row['query']}:{row['location']}")
    for row in greenhouse_reports:
        if row.get('status') == 'complete':
            successful.append(f"greenhouse:{row['board_token']}")

    boards_with_matches = [row for row in all_reports if row.get('matches', 0) > 0]
    warnings = list(linkedin_warnings) + list(indeed_warnings) + list(greenhouse_warnings)
    if not successful:
        warnings.append('No direct board scans completed successfully')
    if not boards_with_matches:
        warnings.append('No direct board matches found for current role filters')
    return {
        'source': 'job_boards',
        'status': 'complete',
        'sources_checked': ['linkedin', 'otta', 'indeed', 'builtin', 'workday', 'greenhouse', 'creative_circle'],
        'sources_successful': successful,
        'jobs_found': len(all_matches),
        'jobs_created': 0,
        'jobs_updated': 0,
        'duplicates_skipped': 0,
        'review_needed': 0,
        'boards_scanned': len(all_reports),
        'boards_with_matches': len(boards_with_matches),
        'board_reports': all_reports,
        'sample_jobs': all_matches[:20],
        'warnings': warnings,
    }
