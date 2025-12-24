import os
import modpack
import secrets

from flask import make_response, render_template, send_from_directory, Flask, request, redirect

filepath = "modlist.md"

author = "CaptainTheDelta"
mc_version = "1.21.11"
name = "test"
version = "0.0.2"

categories = modpack.get_categories(filepath)
mods_slugs = sum([c["mods"] for c in categories], [])
mods = modpack.get_modrinth_infos(mods_slugs, mc_version)

app = Flask("test")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/client')
def selection_page():
    return render_template(
        'client.html',
        categories=categories, 
        mods=mods,
        mc_version=mc_version
    )

@app.post("/pw")
def packwiz_generate():
    # création du dossier
    token = secrets.token_urlsafe(6)
    path = os.path.join("instances", token)
    os.makedirs(path, exist_ok=True)

    mp = modpack.ModPack(path, name, mc_version, author, version)
    mp.add_mods(request.form)
    
    return redirect(f"/pw/{token}/pack.toml", 303)

@app.route('/pw/<path:path>')
def packwiz_raw(path):
    r = make_response(send_from_directory("instances", path))
    r.mimetype = "text/plain"
    return r