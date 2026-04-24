def fetch_runtime_state(rows_to_dicts):
    jobs_header, jobs_rows = rows_to_dicts('Jobs')
    recruiters_header, recruiters_rows = rows_to_dicts('Recruiters')
    signals_header, signals_rows = rows_to_dicts('Signals')
    actions_header, actions_rows = rows_to_dicts('Actions')
    review_header, review_rows = rows_to_dicts('ReviewQueue')
    taskruns_header, taskruns_rows = rows_to_dicts('TaskRuns')
    return {
        'jobs_header': jobs_header,
        'jobs_rows': jobs_rows,
        'recruiters_header': recruiters_header,
        'recruiters_rows': recruiters_rows,
        'signals_header': signals_header,
        'signals_rows': signals_rows,
        'actions_header': actions_header,
        'actions_rows': actions_rows,
        'review_header': review_header,
        'review_rows': review_rows,
        'taskruns_header': taskruns_header,
        'taskruns_rows': taskruns_rows,
    }
