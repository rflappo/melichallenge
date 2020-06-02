from os import path, getcwd
from configparser import ConfigParser


def config(app):
    # Init config
    config = ConfigParser()
    config.read('config.ini')
    db_engine = config['DATABASE'].get('ENGINE', 'postgres')
    db_host = config['DATABASE'].get('HOST', 'localhost')
    db_port = config['DATABASE'].get('PORT', 54320)
    db_user = config['DATABASE'].get('USER', 'melichallenge')
    db_pass = config['DATABASE'].get('PASS', 'melichallenge')
    db_name = config['DATABASE'].get('NAME', 'melichallenge')
    db_uri = f"{db_engine}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Init app
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = path.join(getcwd(), 'files')
