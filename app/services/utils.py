import uuid
import json

def generate_uuid(data):
    normalized = json.dumps(data, sort_keys=True)
    u = uuid.uuid5(uuid.NAMESPACE_DNS, normalized)
    return u.hex[:16]

def get_value(dictionnary, key, default):
    if isinstance(dictionnary, dict):
        return dictionnary.get(key, default)
    return default