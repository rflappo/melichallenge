import os
from flask import Flask
from app.data import db
from app.items.items import uploader_bp


app = Flask('__melichallenge__')
app.config.from_object(os.getenv('APP_SETTINGS'))
db.init_app(app)

app.register_blueprint(uploader_bp, url_prefix="/items")
