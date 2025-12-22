import subprocess

packwiz_bin = "/usr/local/bin/packwiz"

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
    
    def get_mods(self):
        return subprocess.run([
            packwiz_bin, "list"
            ],
            cwd=self.path,
            text=True,
        )
    
    def hash(self, mods=None):
        if mods == None:
            mods = self.get_mods()
        mods = list(sorted(mods))