from app import db
from app.models import *
from app.services.storage import *
from app.services.utils import get_value
import json

def get_db_modpacks():
    """Renvoie la liste des modpacks présents dans la base de donnée."""
    modpacks = db.session.execute(db.select(Modpack)).all()
    return [m[0] for m in modpacks]

def get_modpack(uuid):
    sql_stmt = db.select(Modpack).filter_by(uuid=uuid)
    modpack = db.session.execute(sql_stmt).one_or_none()
    return modpack[0] if modpack else {}

def get_modpack_filename(uuid):
    """Renvoie le nom de fichier assoscié au modpack."""
    return get_modpack(uuid).filename

def get_modpack_game_version(uuid):
    """Renvoie la version de minecraft assosciée au modpack."""
    return get_modpack(uuid).game_version

def get_modpack_mods(uuid):
    mods = {}
    sql_stmt = db.select(ModpackMod.category).filter_by(modpack=uuid).group_by(ModpackMod.category)
    for cat in db.session.execute(sql_stmt).scalars():
        mods[cat] = []

    sql_stmt = db.select(ModpackMod).filter_by(modpack=uuid).order_by(ModpackMod.category)
    for relation in db.session.execute(sql_stmt).all():
        relation = relation[0]
        sql_stmt = db.select(Mod).filter_by(slug=relation.mod)
        if mod := db.session.execute(sql_stmt).one_or_none():
            mod = mod[0].to_dict()
            mod["discuss"] = relation.discuss
            mod["compatibility"] = relation.compatibility

            if mod["title"]:
                mod["updated"] = mod["updated"].strftime("%d/%m/%Y")
                mod["license"] = json.loads(mod["license"])
                print(mod["categories"])
                mod["categories"] = json.loads(mod["categories"])
            if relation.description != "":
                mod["description"] = relation.description
            
            mods[relation.category].append(mod)
    
    return mods

def add_modpack_description(infos, check=None):
    uuid = Modpack.generate_uuid(infos)
    assert check != None and check == uuid, "given uuid different from generated"

    db.session.add(Modpack(uuid=uuid, **infos))
    db.session.commit()

def add_mods(slugs):
    for slug in slugs:
        sql_stmt = db.select(Mod).where(Mod.slug==slug)
        if db.session.execute(sql_stmt).first() == None:
            db.session.add(Mod(slug=slug))
    db.session.commit()

def update_mods(mods_infos):
    for infos in mods_infos:
        sql_stmt = db.select(Mod).filter_by(slug=infos["slug"])

        if mod := db.session.execute(sql_stmt).one_or_none():
            mod = mod[0]
            mod.title = infos["title"]
            mod.description = infos["description"]
            mod.updated = infos["updated"]
            mod.license = infos["license"]
            mod.downloads = infos["downloads"]
            mod.categories = infos["categories"]
            mod.icon_url = infos["icon_url"]

    db.session.commit()


def add_relations_modpack_mod(uuid, slugs):
    for slug in slugs:
        db.session.add(ModpackMod(modpack=uuid, mod=slug))
    db.session.commit()

def update_relations_modpack_mod(uuid, mods_by_categories, mods_infos):
    # on supprime toutes les relations
    sql_stmt = db.select(ModpackMod).where(ModpackMod.modpack==uuid)
    for relation in db.session.execute(sql_stmt).all():
        db.session.delete(relation[0])

    # vérif de la compatibilité
    game_version = get_modpack_game_version(uuid)
    compatible = {}
    for mod in mods_infos:
        compatible[mod["slug"]] = game_version in mod["game_versions"]
    
    # on recrée tout
    for category,mods in mods_by_categories.items():
        for slug,infos in mods.items():
            relation = ModpackMod(
                modpack=uuid,
                mod=slug,
                compatibility=compatible.get(slug),
                category=category,
                description=get_value(infos, key="desc", default=""),
                discuss=get_value(infos, key="discuss", default=False),
            )
            db.session.add(relation)
    db.session.commit()


def remove_db_modpack(uuid):
    modpack = db.session.execute(db.select(Modpack).filter_by(uuid=uuid)).one()[0]
    db.session.delete(modpack)
    db.session.commit()


def clean_unused_mods():
    sql_stmt = db.select(Mod).where(~Mod.modpacks.any())
    for mod in db.session.execute(sql_stmt).all():
        db.session.delete(mod[0])
    db.session.commit()

def get_uuid_from_url(url):
    return url