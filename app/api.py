from flask import Blueprint, request, jsonify

from app.models import Modpack
from app.services.db import *
from app.services.modrinth import get_modrinth_infos, get_mod_dependencies
from app.services.storage import *
from app.services.utils import slugs_only

bp = Blueprint("api", __name__)

@bp.route("/modpacks")
def get_modpacks(internal=False):
    current_files = get_modpacks_files()

    # séparation en trois catégories
    good_ones = [] # ceux qui sont dans le dossier et la bdd
    to_add = [] # ceux seulement dans le dossier
    to_remove = [] # ceux seulement dans la bdd
    
    for m in get_db_modpacks():
        if m.filename in current_files:
            good_ones.append(m)
            current_files.remove(m.filename)
        else:
            to_remove.append(m)
    
    for f in current_files:
        infos = read_modpack_desc(f)
        infos["uuid"] = Modpack.generate_uuid(infos)
        to_add.append(infos)
    
    modpacks = {
        "ok": [m.infos() for m in good_ones],
        "to_add": to_add,
        "to_remove": [m.infos() for m in to_remove],
    }
    return modpacks if internal else jsonify(modpacks)


@bp.post("/modpack/add/<uuid>")
def add_modpack(uuid):
    filename = request.form.get("filename")
    
    mods_by_categories = read_modpack_mods(filename)
    slugs = slugs_only(mods_by_categories)
    desc = read_modpack_desc(filename)
    
    add_modpack_description(desc, check=uuid)
    add_mods(slugs)
    # les mods/modpack sont recréées à chaque update, pas besoin d'init

    update_modpack(uuid, filename)
    return jsonify({"success": True})


@bp.route("/modpack/update/<uuid>", methods=["POST"])
def update_modpack(uuid, filename="", mods_by_categories=[]):
    """Recharge le modpack et mets à jour les mods associés"""
    if mods_by_categories == []:
        if filename == "":
            filename = get_modpack_filename(uuid)
        mods_by_categories = read_modpack_mods(filename)

    slugs = slugs_only(mods_by_categories)
    mods_infos = get_modrinth_infos(slugs)

    update_mods(mods_infos)
    update_relations_modpack_mod(uuid, mods_by_categories, mods_infos)
    clean_unused_mods()
    
    return jsonify({"success": True})


@bp.route("/modpack/remove/<uuid>", methods=["POST"])
def remove_modpack(uuid):
    remove_db_modpack(uuid)
    clean_unused_mods()
    return jsonify({"success": True})