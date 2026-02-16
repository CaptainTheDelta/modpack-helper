from flask import Blueprint, make_response, render_template, request, redirect, send_from_directory

from app.api import *
from app.services.utils import get_instance_uuid
from app.services.packwiz import PackwizModpack
from app.services.storage import move_modpack, get_tmp_folder
from app.services.db import instance_already_exists

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    """Page d'accueil, explication du projet"""
    return render_template("index.html")

@bp.route("/modpacks")
def modpacks_dashboard():
    """Affiche les modpacks existants et propose leur MàJ & suppression"""
    modpacks = get_modpacks(internal=True)
    return render_template("modpacks.html", modpacks=modpacks)

@bp.route("/config/<uuid>")
def modpack_configurator(uuid):
    modpack = get_modpack(uuid)
    if modpack == {}:
        return f"{uuid} n'existe pas, déso"

    mods = get_modpack_mods(uuid)
    return render_template("config.html", modpack=modpack, mods=mods)

@bp.post("/generation")
def generate():
    mods = request.form
    modpack_uuid = request.referrer.split('/')[-1]

    uuid = get_instance_uuid(modpack_uuid, mods)

    if not instance_already_exists(uuid):
        folder = get_tmp_folder()
        print(folder)
        packwiz_modpack = PackwizModpack(folder)
        packwiz_modpack.set_infos(get_modpack_infos(modpack_uuid))
        if packwiz_modpack.set_mods(mods):
            move_modpack(folder, uuid)

    return render_template("generation.html", uuid=uuid)



@bp.route("/mdpk/<url>", defaults={"path": ""})
@bp.route("/mdpk/<url>/<path:path>")
def serve_modpack(url, path):
    path = '/'.join([get_uuid_from_url(url), path])
    r = make_response(send_from_directory("instances", path))
    r.mimetype = "text/plain"
    return r