import json

from app import db
from app.models import Mod, Modpack, ModpackMod, License
from app.services.utils import generate_uuid

def add_all(slugs):
    for slug in slugs:
        sql_stmt = db.select(Mod).where(Mod.slug==slug)
        if db.session.execute(sql_stmt).first() == None:
            db.session.add(Mod(slug=slug))
    db.session.commit()

def get_license(infos_license):
    uuid = generate_uuid(infos_license)    
    sql_stmt = db.select(License).where(License.uuid==uuid)
    
    license = db.session.execute(sql_stmt).one_or_none()

    if license:
        license = license[0]
    else:
        license = License(
            uuid=uuid,
            id=infos_license["id"],
            name=infos_license["name"],
            url=infos_license["url"]
        )
        db.session.add(license)
        db.session.commit()
    return license

def update_all(mods_infos):
    for infos in mods_infos:
        sql_stmt = db.select(Mod).filter_by(slug=infos["slug"])

        if row := db.session.execute(sql_stmt).one_or_none():
            mod = row[0]
            mod.title = infos["title"]
            mod.description = infos["description"]
            mod.updated = infos["updated"]
            mod.downloads = infos["downloads"]
            mod.categories = infos["categories"]
            mod.icon_url = infos["icon_url"]
            mod.license = get_license(infos["license"])

    db.session.commit()

def clean_unused():
    sql_stmt = db.select(Mod).where(~Mod.modpacks.any())
    for mod in db.session.execute(sql_stmt).all():
        db.session.delete(mod[0])
    db.session.commit()

def clean_unused_licenses():
    sql_stmt = db.select(License).where(~License.mods.any())
    for row in db.session.execute(sql_stmt).all():
        db.session.delete(row[0])
    db.session.commit()