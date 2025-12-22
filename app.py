import os
import modpack
import requests
import json
import secrets
import tempfile

from flask import make_response, render_template, send_from_directory, Flask, request, redirect

filepath = "modlist.md"

author = "CaptainTheDelta"
mc_version = "1.21.11"
name = "test"
version = "0.0.1"

with open(filepath, 'r') as f:
    data = f.read().split("#")[1:]
    categories = []
    for chunk in data:
        lines = map(str.strip, filter(lambda t: t != "", chunk.splitlines()))
        cat = next(lines)
        categories.append({
            "name": cat,
            "mods": list(lines)
            }
        )

mods = sum([c["mods"] for c in categories], [])

url = "https://api.modrinth.com/v2/projects"
params = {"ids": json.dumps(mods)}
headers = {"User-Agent": "CaptainTheDelta/modpack-helper/v0.0.1"}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()
projects = response.json()

mods = {}
from pprint import pp
for mod in projects:
    mod["compatibility"] = mc_version in mod["game_versions"]
    mod["updated"] = mod["updated"][:10]
    mod["versions"] = []
    mod["body"] = ""
    mods[mod["slug"]] = mod
    mod["server_only"] = (mod["client_side"] == "unsupported" and mod["server_side"] == "required")
    # if mod["slug"] in ["bunk-beds", "chunky", "distanthorizons", "hardcore-revival", "lithium"]:
    #     print(mod["title"].center(30,"="))
    #     print(mod["client_side"])
    #     print(mod["server_side"])

for i,cat in enumerate(categories):
    m_cat = []
    for mod in cat["mods"]:
        m_cat.append(mods[mod])
    categories[i]["mods"] = m_cat

app = Flask("test")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/client')
def selection_page():
    return render_template('client.html', categories=categories)

@app.route('/server')
def server_configurator():
    return render_template('server.html')

@app.post("/pw")
def packwiz_generate():
    # TODO
    token = secrets.token_urlsafe(8)
    path = os.path.join("static", token)
    os.makedirs(path, exist_ok=True)

    mp = modpack.ModPack(path, name, mc_version, author, version)
    for m in request.form:
        mp.add(m)
    
    return redirect(f"/pw/{token}/pack.toml", 303)

@app.route('/pw/<path:path>')
def packwiz_raw(path):

    r = make_response(send_from_directory("instances", path))
    r.mimetype = "text/plain"
    return r

@app.route("/config")
def menu_configs():
    return "tous les liens vers les configs"

@app.route("/config/<token>")
def show_config(token):
    return "config avec lien raw en haut"