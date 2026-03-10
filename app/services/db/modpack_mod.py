from app import db
from app.models import ModpackMod
from app.services.utils import get_value

import app.services.db.modpack as db_modpack

def add_relations_modpack_mod(uuid: str, slugs: list[str]):
    """Adds the relation between all the mods and the modpack.

    This relation will be augmented with additionnal informations :
    compatibility, custom description, etc.

    Args:
        uuid (str): Modpack identifier.
        slugs (list[str]): List of slugs.
    """
    for slug in slugs:
        db.session.add(ModpackMod(modpack=uuid, mod=slug))
    db.session.commit()

def update_relations(uuid: str, game_version: str, mods_by_categories: dict, mods_infos: list[dict]):
    """Adds information for each mod modpack relation.

    Args:
        uuid (str): Modpack instance
        game_version (str): String reprensenting game version (ex: "1.21.11")
        mods_by_categories (dict): {category:[slugs]}
        mods_infos (list[dict]): [{slug:value, infos:...}]
    """
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