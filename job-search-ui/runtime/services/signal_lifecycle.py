from runtime.domain.signals import signal_status_from_confidence


def ensure_signal(parsed, classification, linked_job_id, signal_ids, signals_rows, new_signals, signals_header, update_row, next_id):
    evidence_ref = f"thread:{parsed['thread_id']}|message:{parsed['message_id']}"
    for row in signals_rows:
        if row['values'].get('evidence_ref', '') == evidence_ref:
            updated = row['values'].copy()
            updated['source'] = parsed['source']
            updated['signal_type'] = classification['signal_type']
            updated['company'] = parsed['company']
            updated['role'] = parsed['role']
            updated['date'] = parsed['date']
            updated['summary'] = classification['summary']
            updated['status'] = signal_status_from_confidence(classification)
            if linked_job_id:
                updated['job_id'] = linked_job_id
            row_values = [updated.get(col, '') for col in signals_header]
            update_row('Signals', row['row_index'], row_values)
            row['values'] = updated
            return False, row['values'].get('signal_id', ''), True
    for row in new_signals:
        if len(row) > 7 and row[7] == evidence_ref:
            return False, row[0], False
    signal_id = next_id('signal_', signal_ids + [r[0] for r in new_signals])
    new_signals.append([
        signal_id,
        parsed['source'],
        classification['signal_type'],
        parsed['company'],
        parsed['role'],
        parsed['date'],
        classification['summary'],
        evidence_ref,
        signal_status_from_confidence(classification),
        linked_job_id,
    ])
    return True, signal_id, True
