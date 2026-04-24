def follow_up_needed(signal_type: str) -> bool:
    return signal_type in {'follow_up_opportunity', 'reply_received', 'recruiter_outreach'}
