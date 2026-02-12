import datetime
import json
import requests
from flask import current_app

def get_modrinth_infos(slugs):
    user_agent = current_app.config["USER_AGENT"]
    response = requests.get(
        "https://api.modrinth.com/v2/projects",
        params={"ids": json.dumps(slugs)},
        headers={"User-Agent": user_agent},
    )
    response.raise_for_status()
    
    return [useful_infos(mod) for mod in response.json()]

    # TODO: vérifier qu'il n'y a pas de limitations du nombre de mods à demander en une fois dans l'API

def useful_infos(mod):
    infos = {}
    keys = [
        "slug",
        "title",
        "description",
        "game_versions",
        "updated",
        "license",
        "downloads",
        "categories",
        "icon_url",
    ]
    for key in keys:
        infos[key] = mod[key]

    infos["updated"] = datetime.datetime.fromisoformat(infos["updated"])
    infos["license"] = json.dumps(infos["license"])
    infos["categories"] = json.dumps(infos["categories"])

    return infos

def get_mod_dependencies(slug):
    response = requests.get(
        f"https://api.modrinth.com/v2/projects",
        headers={"User-Agent": f"{user}/modpack-helper/v{version}"},
    )
    response.raise_for_status()
    return useful_infos(response.json())