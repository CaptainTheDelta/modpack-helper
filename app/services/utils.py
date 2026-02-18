import uuid
import json
from dataclasses import asdict as to_dict

def generate_uuid(data):
    normalized = json.dumps(data, sort_keys=True)
    u = uuid.uuid5(uuid.NAMESPACE_DNS, normalized)
    return u.hex[:16]

def generate_modpack_uuid(modpack_infos):
    keys = ["name", "author", "version", "game_version"]
    return generate_uuid([modpack_infos[k] for k in keys])

def generate_instance_uuid(modpack_uuid, mods):
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