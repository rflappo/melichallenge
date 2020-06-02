from app import app
from flask.cli import FlaskGroup

cli = FlaskGroup(app)


@cli.command()
def initialize_db():
    ''' [Just Once docker is up] Create the initial table based the model '''
    from app import db
    db.create_all()


if __name__ == '__main__':
    cli()
