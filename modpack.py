import subprocess
import requests
import json

packwiz_bin = "/usr/local/bin/packwiz"

def get_categories(path):
    with open(path, 'r') as f:
        data = f.read().split("#")[1:]
        categories = []
        for chunk in data:
            lines = map(str.strip, filter(lambda t: t != "", chunk.splitlines()))
            cat = next(lines)
            categories.append({
                "name": cat,
                "mods": list(lines),
                }
            )
    return categories

def get_modrinth_infos(mods, mc_version):
    response = requests.get(
        "https://api.modrinth.com/v2/projects",
        params={"ids": json.dumps(mods)},
        headers={"User-Agent": "CaptainTheDelta/modpack-helper/v0.0.2"},
    )
    response.raise_for_status()
    
    mods_infos = {}
    for mod in response.json():
        mod["compatibility"] = mc_version in mod["game_versions"]
        mod["updated"] = mod["updated"][:10]
        mods_infos[mod["slug"]] = mod
    return mods_infos

class ModPack():
    def __init__(self, path, name, mc_version, author, version):
        self.path = path

        subprocess.run([
            packwiz_bin, "init",
            "--mc-version", mc_version,
            "--name", name,
            "--version", version,
            "--author", author,
            "--modloader", "fabric", "--fabric-latest",
            "--reinit",
            ],
            cwd=self.path,
        )
    
    def add(self, mod):
        return subprocess.run([
            packwiz_bin, "modrinth", "add", "-y",
            mod,
            ],
            cwd=self.path,
        )

    def add_mods(self, mods):
        for mod in mods:
            self.add(mod)