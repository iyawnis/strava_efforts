import json
from store import redis

hardcoded_segments = ['7550717']

stored_segments = redis.get('segments')

if not stored_segments:
    stored_segments = json.dumps([])

stored_segments = json.loads(stored_segments)
new_segments =  set(hardcoded_segments) - set(stored_segments)

new_stored_segments = stored_segments + list(new_segments)

redis.set('segments', json.dumps(new_stored_segments))

