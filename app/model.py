from app.data import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, nullable=False)
    site = db.Column(db.String(length=16), nullable=False)
    price = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    name = db.Column(db.String(length=128))
    description = db.Column(db.String(length=64))
    nickname = db.Column(db.String(length=50))

    __table_args__ = (
        db.PrimaryKeyConstraint('site', 'id'),
        {}
    )

    @classmethod
    def create_item(cls, site, id, db_session=None):
        item = Item(site=site, id=id)

        if db_session:
            db_session.add(item)
        else:
            db.session.add(item)

        if db_session:
            db_session.commit()
        else:
            db.session.commit()

        return item

    @classmethod
    def get_or_create_item(cls, site, id, db_session=None):
        item = cls.get_item(site, id)
        if not item:
            item = cls.create_item(site, id, db_session)

        return item

    @classmethod
    def get_item(cls, site, id):
        item = cls.query.filter(cls.site == site).filter(cls.id == id)
        return item.first()

    def __str__(self):
        return "{"\
               f"'id':'{self.id}'"\
               f", 'site':'{self.site}'"\
               f", 'price':'{self.price}'"\
               f", 'name':'{self.name}'"\
               f", 'description':'{self.description}'"\
               f", 'nickname':'{self.nickname}'"\
               "}"
