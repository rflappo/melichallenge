import os


class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # UPLOADS_FOLDER = os.path.join(os.getcwd(), 'uploads')
    DEBUG = True
