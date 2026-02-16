import uuid
import json

def generate_uuid(data):
    normalized = json.dumps(data, sort_keys=True)
    u = uuid.uuid5(uuid.NAMESPACE_DNS, normalized)
    return u.hex[:16]

def get_instance_uuid(modpack_uuid, mods):
    return generate_uuid([modpack_uuid, mods])

def get_value(dictionnary, key, default):
    if isinstance(dictionnary, dict):
        return dictionnary.get(key, default)
    return default

def slugs_only(categories : dict):
    """Renvoie la liste des slugs."""
    slugs = []
    for c in categories:
        slugs.extend(categories[c].keys())
    return slugs