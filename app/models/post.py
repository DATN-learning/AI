from app.extensions import db
from app.models.user import User
from app.models.classroom import ClassRoom
from app.models.subject import Subject
from app.models.CommentPost import CommentPost
from app.models.post_analytic import PostAnalysisData

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    id_post = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_room_id = db.Column(db.Integer, db.ForeignKey('class_rooms.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category_post = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('User', back_populates='posts')
    class_room = db.relationship('ClassRoom', back_populates='posts')
    subject = db.relationship('Subject', back_populates='posts')
    comments = db.relationship('CommentPost', back_populates='post')
    analytics = db.relationship('PostAnalysisData', back_populates='post')
