#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.append('/Users/jtemp/.openclaw/workspace/job-search-ui')

from runtime.adapters.job_boards import load_job_board_targets, scan_greenhouse_targets

ROOT = Path('/Users/jtemp/.openclaw/workspace/job-search-ui')
TARGETS = ROOT / 'runtime' / 'job_board_targets.json'


def main():
    config = load_job_board_targets(TARGETS)
    matches, board_reports, warnings = scan_greenhouse_targets(config)
    print(json.dumps({
        'config_path': str(TARGETS),
        'matches_found': len(matches),
        'board_reports': board_reports,
        'sample_matches': matches[:25],
        'warnings': warnings,
    }, indent=2))


if __name__ == '__main__':
    main()
