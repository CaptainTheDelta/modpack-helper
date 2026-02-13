import os
import yaml
from flask import current_app
from app.services.utils import slugs_only

def read_modpack_desc(filename, add_path=True):
    """Renvoie la description du modpack contenue dans le fichier."""
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(upload_folder, filename)
    
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    infos = config.get("infos")
    if add_path:
        infos["filename"] = filename
    
    return infos

def read_modpack_mods(filename):
    """Renvoie la liste des mods organisée par catégories."""
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(upload_folder, filename)
    
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config.get("mods")
    
def get_modpacks_files():
    """Renvoie la liste des noms de fichiers contenus dans le dossier
    défini par UPLOAD_FOLDER."""
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    scan = os.scandir(upload_folder)
    return [f.name for f in scan if f.is_file()]