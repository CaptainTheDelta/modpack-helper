from flask import Blueprint, render_template, request

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

@bp.route("/mdpk/<uuid>")
def modpack_serve(uuid):
    "Lien du modpack généré et prêt à l'emploi"
    return f"Under construction page for {uuid}"