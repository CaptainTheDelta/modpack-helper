from app import db
from app.models import Instance, CustomUrl

def get_all():
    """Renvoie la liste des modpacks présents dans la base de donnée."""
    instances = db.session.execute(db.select(Instance)).all()
    return [to_dict(row[0]) for row in instances]

def get_uuid(url):
    if exists(url):
        return url
    sql_stmt = db.select(CustomUrl.instance).where(CustomUrl.url==url)
    instance_url = db.session.execute(sql_stmt).one_or_none()
    return instance_url[0] if instance_url else ""

def add(instance_uuid, modpack_uuid):
    db.session.add(Instance(uuid=instance_uuid, modpack=modpack_uuid))
    db.session.commit()

def exists(uuid):
    sql_stmt = db.select(Instance).where(Instance.uuid==uuid)
    return db.session.execute(sql_stmt).first() != None