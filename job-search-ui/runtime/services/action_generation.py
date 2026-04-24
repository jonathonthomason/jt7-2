from runtime.domain.actions import (
    ACTION_REQUIRED_SIGNAL_TYPES,
    action_urgency,
    canonical_action_due_at,
    canonical_action_status,
    proposed_action_instruction,
)


ACTION_ROW_COLUMNS = ['action_id', 'job_id', 'company', 'instruction', 'reason', 'urgency', 'status', 'created_at', 'due_at', 'owner']


def build_action_row(action_id, job_id, company, classification, run_at, signal_id=''):
    return [
        action_id,
        job_id,
        company,
        proposed_action_instruction(classification['signal_type']),
        f"Signal type: {classification['signal_type']} | signal_id: {signal_id}".strip(),
        action_urgency(classification['signal_type']),
        canonical_action_status(classification, job_id),
        run_at.isoformat(),
        canonical_action_due_at(classification, run_at),
        'JT7',
    ]


def action_required(signal_type):
    return signal_type in ACTION_REQUIRED_SIGNAL_TYPES
