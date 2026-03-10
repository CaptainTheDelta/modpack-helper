from app import db
from app.models import Instance, CustomUrl

def get_all() -> list[dict]:
    """Returns all the instances as dictionnary in database.

    Returns:
        list[dict]: List of all instances.
    """
    instances = db.session.execute(db.select(Instance)).all()
    return [to_dict(row[0]) for row in instances]

def get_uuid(url: str) -> str:
    """Returns the uuid associated with url if it exists in databse.

    Three scenari:
        url is a uuid
        url is CustomUrl
        url does not exists in database.

    Args:
        url (str): url to link to an uuid.

    Returns:
        str: uuid or empty string.
    """
    if exists(url):
        return url
    sql_stmt = db.select(CustomUrl.instance).where(CustomUrl.url==url)
    instance_url = db.session.execute(sql_stmt).one_or_none()
    return instance_url[0] if instance_url else ""

def add(instance_uuid: str, modpack_uuid: str):
    """Add a link between a modpack and an instance.

    Usually called at the creation of the instance.

    Args:
        instance_uuid (str): Instance identifier.
        modpack_uuid (str): Modpack identifier.
    """
    db.session.add(Instance(uuid=instance_uuid, modpack=modpack_uuid))
    db.session.commit()

def exists(uuid: str) -> bool:
    """Returns if instance already exists in database.

    Args:
        uuid (str): Instance identifier.

    Returns:
        bool: Existence in database.
    """
    sql_stmt = db.select(Instance).where(Instance.uuid==uuid)
    return db.session.execute(sql_stmt).first() != None