from app.extensions import db

class CommentPost(db.Model):
    __tablename__ = 'comment_posts'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text)
    approved = db.Column(db.Boolean, default=False)
    spam = db.Column(db.Boolean, default=False)
    trash = db.Column(db.Boolean, default=False)
    notify = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')
