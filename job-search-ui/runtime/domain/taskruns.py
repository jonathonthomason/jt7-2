from dataclasses import dataclass


@dataclass(frozen=True)
class TaskRunRecord:
    task_run_id: str
    task_type: str
    status: str
    last_run_at: str
    next_run_at: str
    result_summary: str
    outputs_ref: str
