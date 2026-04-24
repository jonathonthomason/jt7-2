def next_id(prefix, existing_ids):
    max_n = 0
    for value in existing_ids:
        if isinstance(value, str) and value.startswith(prefix):
            tail = value.replace(prefix, '')
            if tail.isdigit():
                max_n = max(max_n, int(tail))
    return f'{prefix}{max_n + 1:03d}'
