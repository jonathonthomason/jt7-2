def collect_gmail_messages(query, gog_json):
    return gog_json(['gog', 'gmail', 'messages', 'search', query, '--max', '100', '--json']).get('messages', [])


def collect_gmail_threads(query, gog_json):
    return gog_json(['gog', 'gmail', 'search', query, '--max', '100', '--json']).get('threads', [])


def build_thread_map(threads, messages):
    thread_map = {t['id']: {'thread': t, 'messages': []} for t in threads}
    for m in messages:
        thread_map.setdefault(m['threadId'], {'thread': {'id': m['threadId'], 'labels': m.get('labels', [])}, 'messages': []})
        thread_map[m['threadId']]['messages'].append(m)
    return thread_map
