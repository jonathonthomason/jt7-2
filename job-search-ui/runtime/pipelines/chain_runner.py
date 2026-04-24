def build_task_summary(task_name, gmail_report, calendar_report, git_report=None, mirror_report=None):
    if task_name == 'EMAIL_SIGNAL_SCAN':
        return f"Email scan executed, {gmail_report['signals_created']} signals, {gmail_report['jobs_created']} jobs created, {gmail_report['jobs_updated']} jobs updated"
    if task_name == 'CALENDAR_SIGNAL_SCAN':
        return f"Calendar scan executed, {calendar_report['matched_jobs']} jobs matched, {calendar_report['updates_written']} job updates"
    if task_name == 'JOB_BOARD_SIGNAL_SCAN':
        return 'Job board scan executed from current configured sources when available'
    if task_name == 'SIGNAL_CLASSIFICATION':
        return f"Signal classification completed, {gmail_report['review_needed_count']} review-needed signals"
    if task_name == 'PIPELINE_STATE_SYNC':
        return 'Pipeline reconciliation pass completed using probabilistic matching rules'
    if task_name == 'PIPELINE_UPDATE':
        return 'Pipeline update pass completed against live tracker model with real Sheets CRUD'
    if task_name == 'LOCAL_MIRROR_SYNC' and mirror_report:
        return f"Local mirror updated for tabs: {', '.join(mirror_report['tabs_mirrored'])}"
    if task_name == 'GIT_COMMIT_SYNC' and git_report:
        return git_report['summary']
    if task_name == 'ACTION_GENERATION':
        total_actions = gmail_report['actions_created'] + calendar_report['actions_created']
        return f'Action generation pass completed, {total_actions} actions created'
    if task_name == 'PRIORITY_SURFACING':
        return 'Priority surfacing pass completed'
    if task_name == 'PASS_LOGGER':
        return 'Pass logger completed with detailed transparency report'
    return 'Executed'
