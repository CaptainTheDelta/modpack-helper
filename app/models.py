from app import db
from app.services.utils import generate_uuid
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ModpackMod(db.Model):
    id: int = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mod: str = db.Column(db.String, db.ForeignKey('mod.slug'), nullable=False)
    modpack: str = db.Column(db.String, db.ForeignKey('modpack.uuid'), nullable=False)
    compatibility: bool = db.Column(db.Boolean)
    category: str = db.Column(db.String)
    description: str = db.Column(db.String)
    discuss: bool = db.Column(db.Boolean)

@dataclass
class Modpack(db.Model):
    """Contient la description d'un modpack."""
    uuid: str = db.Column(db.String(8), primary_key=True)
    filename: str = db.Column(db.String(255), nullable=False)

    name: str = db.Column(db.String, nullable=False)
    author: str = db.Column(db.String, nullable=False)
    version: str = db.Column(db.String, nullable=False)
    game_version: str = db.Column(db.String, nullable=False)

    mods = db.relationship("Mod", back_populates='modpacks', secondary=ModpackMod.__table__)

@dataclass
class Mod(db.Model):
    slug: str = db.Column(db.String, primary_key=True)

    title: str = db.Column(db.String)
    description: str = db.Column(db.String)
    updated: datetime = db.Column(db.DateTime)
    license_uuid: str = db.Column(db.String, db.ForeignKey('license.uuid'))
    downloads: int = db.Column(db.Integer)
    categories: str = db.Column(db.String)
    icon_url: str = db.Column(db.String)

    license = db.relationship("License", back_populates="mods")
    modpacks = db.relationship("Modpack", back_populates='mods', secondary=ModpackMod.__table__)

@dataclass
class Instance(db.Model):
    uuid: str = db.Column(db.String, primary_key=True)
    modpack: str = db.Column(db.String, db.ForeignKey('modpack.uuid'), nullable=False)

@dataclass
class CustomUrl(db.Model):
    url: str = db.Column(db.String, primary_key=True)
    instance: str = db.Column(db.String, db.ForeignKey('instance.uuid'), nullable=False)

@dataclass
class License(db.Model):
    uuid: str = db.Column(db.String, primary_key=True)
    id: str = db.Column(db.String)
    name: str = db.Column(db.String)
    url: str = db.Column(db.String)

    mods = db.relationship("Mod")