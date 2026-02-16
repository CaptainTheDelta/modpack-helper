from app import db
from app.services.utils import generate_uuid

class ModpackMod(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mod = db.Column(db.String, db.ForeignKey('mod.slug'), nullable=False)
    modpack = db.Column(db.String, db.ForeignKey('modpack.uuid'), nullable=False)
    compatibility = db.Column(db.Boolean)
    category = db.Column(db.String)
    description = db.Column(db.String)
    discuss = db.Column(db.Boolean)

class Modpack(db.Model):
    """Contient la description d'un modpack."""
    uuid = db.Column(db.String(8), primary_key=True)
    filename = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False)
    game_version = db.Column(db.String, nullable=False)

    mods = db.relationship("Mod", back_populates='modpacks', secondary=ModpackMod.__table__)

    def infos(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "author": self.author,
            "version": self.version,
            "game_version": self.game_version,
            "filename": self.filename,
        }   

    @staticmethod
    def generate_uuid(data):
        values = {}
        for k in ["name", "author", "version", "game_version", "filename"]:
            values[k] = data.get(k, '')
        return generate_uuid(values)

class Mod(db.Model):
    slug = db.Column(db.String, primary_key=True)

    title = db.Column(db.String)
    description = db.Column(db.String)
    updated = db.Column(db.DateTime)
    license = db.Column(db.String)
    downloads = db.Column(db.Integer)
    categories = db.Column(db.String)
    icon_url = db.Column(db.String)

    modpacks = db.relationship("Modpack", back_populates='mods', secondary=ModpackMod.__table__)

    
    def to_dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

class Instance(db.Model):
    uuid = db.Column(db.String, primary_key=True)
    modpack = db.Column(db.String, nullable=False)