from flask import Blueprint, request, jsonify

from app.models import Modpack
from app.services.modrinth import get_modrinth_infos, get_mod_dependencies
from app.services.storage import *
from app.services.utils import slugs_only, generate_modpack_uuid, to_dict

import app.services.db.mod as db_mod
import app.services.db.modpack as db_modpack
import app.services.db.modpack_mod as db_modpack_mod

bp = Blueprint("api", __name__)

@bp.route("/modpacks")
def get_modpacks(internal=False):
    current_files = get_modpacks_files()

    # séparation en trois catégories
    good_ones = [] # ceux qui sont dans le dossier et la bdd
    to_add = [] # ceux seulement dans le dossier
    to_remove = [] # ceux seulement dans la bdd
    
    for m in db_modpack.get_all():
        if m["filename"] in current_files:
            good_ones.append(m)
            current_files.remove(m["filename"])
        else:
            to_remove.append(m)
    
    for f in current_files:
        infos = read_modpack_desc(f)
        infos["uuid"] = generate_modpack_uuid(infos)
        to_add.append(infos)
    
    modpacks = {
        "ok": good_ones,
        "to_add": to_add,
        "to_remove": to_remove,
    }
    return modpacks if internal else jsonify(modpacks)


@bp.post("/modpack/add/<uuid>")
def add_modpack(uuid):
    filename = request.form.get("filename")
    
    mods_by_categories = read_modpack_mods(filename)
    slugs = slugs_only(mods_by_categories)
    desc = read_modpack_desc(filename)
    
    db_modpack.add_description(desc, check=uuid)
    db_mod.add_all(slugs)
    # les mods/modpack sont recréées à chaque update, pas besoin d'init

    update_modpack(uuid, filename)
    return jsonify({"success": True})


@bp.route("/modpack/update/<uuid>", methods=["POST"])
def update_modpack(uuid, filename="", mods_by_categories=[]):
    """Recharge le modpack et mets à jour les mods associés"""
    if mods_by_categories == []:
        if filename == "":
            filename = db_modpack.get_filename(uuid)
        mods_by_categories = read_modpack_mods(filename)

    slugs = slugs_only(mods_by_categories)
    mods_infos = get_modrinth_infos(slugs)

    db_mod.update_all(mods_infos)
    game_version = ""
    db_modpack_mod.update_relations(uuid, game_version, mods_by_categories, mods_infos)
    db_mod.clean_unused()
    
    return jsonify({"success": True})


@bp.route("/modpack/remove/<uuid>", methods=["POST"])
def remove_modpack(uuid):
    db_modpack.remove(uuid)
    db_mod.clean_unused()
    db_mod.clean_unused_licenses()
    return jsonify({"success": True})