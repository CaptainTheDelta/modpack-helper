import json

from app import db
from app.models import Mod, Modpack, ModpackMod

def add_all(slugs):
    for slug in slugs:
        sql_stmt = db.select(Mod).where(Mod.slug==slug)
        if db.session.execute(sql_stmt).first() == None:
            db.session.add(Mod(slug=slug))
    db.session.commit()

def update_all(mods_infos):
    for infos in mods_infos:
        sql_stmt = db.select(Mod).filter_by(slug=infos["slug"])

        if row := db.session.execute(sql_stmt).one_or_none():
            mod = row[0]
            mod.title = infos["title"]
            mod.description = infos["description"]
            mod.updated = infos["updated"]
            mod.license = infos["license"]
            mod.downloads = infos["downloads"]
            mod.categories = infos["categories"]
            mod.icon_url = infos["icon_url"]

    db.session.commit()

def clean_unused():
    sql_stmt = db.select(Mod).where(~Mod.modpacks.any())
    for mod in db.session.execute(sql_stmt).all():
        db.session.delete(mod[0])
    db.session.commit()