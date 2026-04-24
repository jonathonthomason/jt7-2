from runtime.domain.actions import canonical_action_due_at


def normalized_action_status(action, job, linked_signals):
    job_status = (job.get('status', '') or '').strip().lower()
    instruction = (action.get('instruction', '') or '').strip().lower()
    signal_types = {((signal.get('signal_type', '') or '').strip()) for signal in linked_signals}

    if job_status in {'rejected'}:
        return 'done'
    if job_status in {'applied', 'offer'}:
        return 'waiting'
    if 'review opportunity and decide whether to apply' in instruction and job_status in {'cold'}:
        return 'open'
    if 'prepare for interview' in instruction or job_status in {'interviewing'} or 'interview_scheduling' in signal_types or 'reschedule' in signal_types:
        return 'open'
    if 'reply to recruiter outreach' in instruction or 'respond to hiring manager communication' in instruction:
        return 'open'
    if 'send follow-up response' in instruction or 'review reply and respond' in instruction:
        return 'open'
    return action.get('status', 'open') or 'open'


def normalized_action_reason(action, linked_signals):
    existing = action.get('reason', '') or ''
    signal_ids = [signal.get('signal_id', '') for signal in linked_signals if signal.get('signal_id', '')]
    signal_type = next((signal.get('signal_type', '') for signal in linked_signals if signal.get('signal_type', '')), '')
    if signal_ids and signal_type:
        return f"Signal type: {signal_type} | signal_id: {signal_ids[-1]}"
    if signal_ids:
        return f"signal_id: {signal_ids[-1]}"
    return existing


def normalized_action_due_at(action, linked_signals, run_at):
    signal_type = next((signal.get('signal_type', '') for signal in linked_signals if signal.get('signal_type', '')), '')
    if signal_type:
        return canonical_action_due_at({'signal_type': signal_type}, run_at)
    return action.get('due_at', '') or ''
