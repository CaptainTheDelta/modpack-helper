class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "modpacks"
    USER_AGENT = "CaptainTheDelta/modpack-helper/v0.9"