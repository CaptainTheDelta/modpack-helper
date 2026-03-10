import json

from app import db
from app.models import Mod, Modpack, ModpackMod, License
from app.services.utils import generate_uuid

def add_all(slugs: list[str]):
    """Add each slug in database if not already in it.

    Args:
        slugs (list[str]): Slugs designing a mod.
    """
    for slug in slugs:
        sql_stmt = db.select(Mod).where(Mod.slug==slug)
        if db.session.execute(sql_stmt).first() == None:
            db.session.add(Mod(slug=slug))
    db.session.commit()

def get_license(infos_license: dict) -> License:
    """Return the License object associated with infos_license given.

    If it is not yet in database, adds it.

    Args:
        infos_license (dict): id, name and url of a license.

    Returns:
        License: License object.
    """
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

def update_all(mods_infos: list[dict]):
    """Update the corresponding mods in database, based on mods_infos.

    Args:
        mods_infos (list[dict]): List of 'column':value for each mods.
    """
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
    """Removes unused mods from database."""
    sql_stmt = db.select(Mod).where(~Mod.modpacks.any())
    for mod in db.session.execute(sql_stmt).all():
        db.session.delete(mod[0])
    db.session.commit()

def clean_unused_licenses():
    """Removes unused licenses from database."""
    sql_stmt = db.select(License).where(~License.mods.any())
    for row in db.session.execute(sql_stmt).all():
        db.session.delete(row[0])
    db.session.commit()