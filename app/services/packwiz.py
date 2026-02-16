import subprocess
from flask import current_app


class PackwizModpack():
    def __init__(self, folder):
        self.folder = folder
        self.bin = current_app.config["PACKWIZ_BIN"]
    
    def set_infos(self, infos):
        subprocess.run([
            self.bin, "init",
            "--mc-version", infos["game_version"],
            "--name", infos["name"],
            "--version", infos["version"],
            "--author", infos["author"],
            "--modloader", "fabric", "--fabric-latest",
            "--reinit",
            ],
            cwd=self.folder,
        )

    def set_mods(self, mods):
        for mod in mods:
            self.add(mod)
        return True

    def add(self, mod):
        return subprocess.run([
            self.bin, "modrinth", "add", "-y",
            mod,
            ],
            cwd=self.folder,
        )