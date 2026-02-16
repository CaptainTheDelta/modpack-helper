from flask import Blueprint, make_response, render_template, request, redirect, send_from_directory

from app.api import *

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
    r = request.form
    print(r)
    return render_template("generation.html", slugs=request.form.keys())

@bp.route("/mdpk/<url>", defaults={"path": ""})
@bp.route("/mdpk/<url>/<path:path>")
def serve_modpack(url, path):
    path = '/'.join([get_uuid_from_url(url), path])
    r = make_response(send_from_directory("instances", path))
    r.mimetype = "text/plain"
    return r