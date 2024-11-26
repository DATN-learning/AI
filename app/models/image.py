from app.extensions import db

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.BigInteger, primary_key=True)
    id_query_image = db.Column(db.String(255))
    url_image = db.Column(db.String(255))
