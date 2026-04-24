def job_board_scan_report():
    return {
        'source': 'job_boards',
        'status': 'complete',
        'sources_checked': ['linkedin', 'indeed', 'builtin', 'workday', 'greenhouse', 'creative_circle'],
        'sources_successful': [],
        'jobs_found': 0,
        'jobs_created': 0,
        'jobs_updated': 0,
        'duplicates_skipped': 0,
        'review_needed': 0,
        'warnings': ['Board adapters still pending beyond Gmail-delivered board signals'],
    }
