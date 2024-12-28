from app.extensions import db
from app.models.CommentPost import CommentPost

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Relationships
    posts = db.relationship('Post', back_populates='user')
    comments = db.relationship('CommentPost', back_populates='user')
    ratings = db.relationship('Rating', back_populates='user', lazy='dynamic')