from app.extensions import db
from app.models.user import User
from app.models.lesstion_chapter import LesstionChapter

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.BigInteger, primary_key=True)
    rating_id = db.Column(db.BigInteger, nullable=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    lesstion_chapter_id = db.Column(db.BigInteger, db.ForeignKey('lesstion_chapters.id'), nullable=False) 
    content = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='ratings')
    lesson_chapter = db.relationship('LesstionChapter', back_populates='ratings')

