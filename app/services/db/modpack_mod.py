from app import db
from app.models import ModpackMod
from app.services.utils import get_value

import app.services.db.modpack as db_modpack

def add_relations_modpack_mod(uuid, slugs):
    for slug in slugs:
        db.session.add(ModpackMod(modpack=uuid, mod=slug))
    db.session.commit()

def update_relations(uuid, game_version, mods_by_categories, mods_infos):
    # on supprime toutes les relations
    sql_stmt = db.select(ModpackMod).where(ModpackMod.modpack==uuid)
    for relation in db.session.execute(sql_stmt).all():
        db.session.delete(relation[0])

    # vérif de la compatibilité
    game_version = db_modpack.get_game_version(uuid)
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
                description=get_value(infos, key="desc", default=""), # TODO bouger la 
                discuss=get_value(infos, key="discuss", default=False),
            )
            db.session.add(relation)
    db.session.commit()