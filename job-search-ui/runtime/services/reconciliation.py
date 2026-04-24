def find_best_job_match(parsed, jobs_rows, score_job_match):
    best = None
    best_score = 0.0
    for row in jobs_rows:
        score = score_job_match(parsed, row)
        if score > best_score:
            best_score = score
            best = row
    return best, best_score
