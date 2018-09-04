import json
from store import redis

hardcoded_segments = ['7550717', '1184996', '1444413', '1552278', '1329405', '1087375', '1164504', '998208', '14021755', '1018221', '1329459', '1141197', '1900485', '2413551', '1164862']

stored_segments = redis.get('segments')

if not stored_segments:
    stored_segments = json.dumps([])

stored_segments = json.loads(stored_segments)
new_segments =  set(hardcoded_segments) - set(stored_segments)

new_stored_segments = stored_segments + list(new_segments)

redis.set('segments', json.dumps(new_stored_segments))

