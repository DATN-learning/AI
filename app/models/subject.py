from app.extensions import db

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    id_subject = db.Column(db.Integer, nullable=False)
    class_room_id = db.Column(db.Integer, nullable=False)
    name_subject = db.Column(db.String(255), nullable=False)
    logo_image = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    chapters = db.relationship('ChapterSubject', back_populates='subject')
    posts = db.relationship('Post', back_populates='subject')