import os
from flask import Blueprint, current_app, make_response, render_template, request, redirect, send_from_directory

import app.api as api
from app.services.utils import generate_instance_uuid
from app.services.packwiz import PackwizModpack
from app.services.storage import move_modpack, get_tmp_folder

import app.services.db.modpack as db_modpack
import app.services.db.instance as db_instance

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    """Page d'accueil, explication du projet"""
    return render_template("index.html")

@bp.route("/modpacks")
def modpacks_dashboard():
    """Affiche les modpacks existants et propose leur MàJ & suppression"""
    modpacks = api.get_modpacks(internal=True)
    return render_template("modpacks.html", modpacks=modpacks)

@bp.route("/config/<uuid>")
def modpack_configurator(uuid):
    modpack = db_modpack.get(uuid)
    if modpack == {}:
        return f"{uuid} n'existe pas, déso"

    mods = db_modpack.get_mods(uuid)
    return render_template("config.html", modpack=modpack, mods=mods)

@bp.post("/generation")
def generate():
    mods = request.form
    modpack_uuid = request.referrer.split('/')[-1]
    
    uuid = generate_instance_uuid(modpack_uuid, mods) # TODO changer le nom de fonction

    if not db_instance.exists(uuid):
        db_instance.add(uuid, modpack_uuid)
        folder = get_tmp_folder()
        packwiz_modpack = PackwizModpack(folder)
        packwiz_modpack.set_infos(db_modpack.get_infos(modpack_uuid))
        if packwiz_modpack.set_mods(mods):
            move_modpack(folder, uuid)

    return render_template("generation.html", uuid=uuid)

@bp.route("/mdpk/<url>/<path:path>")
def serve_modpack(url, path):
    folder = current_app.config["DOWNLOAD_FOLDER"]
    path = os.path.join(db_instance.get_uuid(url), path)
    r = make_response(send_from_directory(folder, path))
    r.mimetype = "text/plain"
    return r