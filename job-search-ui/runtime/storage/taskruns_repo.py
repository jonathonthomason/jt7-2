def update_taskruns(run_at, next_at, run_log, rows_to_dicts, next_id, append_rows, iso):
    _, taskruns_rows = rows_to_dicts('TaskRuns')
    taskrun_ids = [r['values'].get('task_run_id', '') for r in taskruns_rows]
    task_run_id = next_id('taskrun_', taskrun_ids)
    inputs_ref = f"gmail:{run_log['sources_checked'][0].get('threads_scanned',0)}|calendar:{run_log['sources_checked'][1].get('events_scanned',0)}"
    outputs_ref = f"signals:{run_log['sources_checked'][0].get('signals_created',0)}|jobs:{run_log['sources_checked'][0].get('jobs_created',0)+run_log['sources_checked'][0].get('jobs_updated',0)}|actions:{run_log['sources_checked'][0].get('actions_created',0)+run_log['sources_checked'][1].get('actions_created',0)}"
    append_rows('TaskRuns', [[
        task_run_id,
        'JT7_CHAIN',
        run_log['status'],
        'high',
        'multi-daily',
        iso(run_at),
        iso(next_at),
        run_log['summary'],
        inputs_ref,
        outputs_ref,
    ]])
    return task_run_id
