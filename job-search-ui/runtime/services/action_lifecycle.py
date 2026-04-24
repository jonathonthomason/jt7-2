from runtime.domain.actions import action_urgency, canonical_action_due_at, canonical_action_status


def apply_action_update(existing_values, classification, run_at, signal_id=''):
    updated = existing_values.copy()
    signal_type = classification.get('signal_type', '')
    updated['reason'] = f"Signal type: {signal_type} | signal_id: {signal_id}".strip()
    updated['urgency'] = action_urgency(signal_type)
    updated['status'] = canonical_action_status(classification, updated.get('job_id', ''))
    updated['due_at'] = canonical_action_due_at(classification, run_at)
    return updated
