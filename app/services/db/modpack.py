import json

from app import db
from app.models import Mod, Modpack, ModpackMod

from app.services.utils import generate_modpack_uuid, to_dict

def get_all():
    """Renvoie la liste des modpacks présents dans la base de donnée."""
    modpacks = db.session.execute(db.select(Modpack)).all()
    return [to_dict(m[0]) for m in modpacks]

def get(uuid):
    sql_stmt = db.select(Modpack).filter_by(uuid=uuid)
    modpack = db.session.execute(sql_stmt).one_or_none()
    return modpack[0] if modpack else {}

def get_filename(uuid):
    """Renvoie le nom de fichier assoscié au modpack."""
    return get(uuid).filename

def get_game_version(uuid):
    """Renvoie la version de minecraft assosciée au modpack."""
    return get(uuid).game_version

def get_infos(uuid):
    return to_dict(get(uuid))

def get_mods(uuid):
    mods = {}
    sql_stmt = db.select(ModpackMod.category).filter_by(modpack=uuid).group_by(ModpackMod.category)
    for cat in db.session.execute(sql_stmt).scalars():
        mods[cat] = []

    sql_stmt = db.select(ModpackMod).filter_by(modpack=uuid).order_by(ModpackMod.category)
    for row in db.session.execute(sql_stmt).all():
        relation = row[0]
        sql_stmt = db.select(Mod).filter_by(slug=relation.mod)
        if row := db.session.execute(sql_stmt).one_or_none():
            mod = to_dict(row[0])
            mod["discuss"] = relation.discuss
            mod["compatibility"] = relation.compatibility

            if mod["title"]:
                mod["updated"] = mod["updated"].strftime("%d/%m/%Y") # FIXME
                mod["license"] = json.loads(mod["license"]) # FIXME
                mod["categories"] = json.loads(mod["categories"]) # FIXME
            if relation.description != "":
                mod["description"] = relation.description
            
            mods[relation.category].append(mod)
    return mods

def add_description(infos, check=None):
    uuid = generate_modpack_uuid(infos) # TODO déplacer la génération de l'uuid
    assert check != None and check == uuid, "given uuid different from generated"

    db.session.add(Modpack(uuid=uuid, **infos))
    db.session.commit()

def remove(uuid):
    modpack = db.session.execute(db.select(Modpack).filter_by(uuid=uuid)).one()[0]
    db.session.delete(modpack)
    db.session.commit()