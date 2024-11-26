from app.extensions import db

class PostAnalysisData(db.Model):
    __tablename__ = 'post_analysis_data'

    id = db.Column(db.Integer, primary_key=True)
    id_post_analysis_data = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    text_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Relationships
    post = db.relationship('Post', back_populates='analytics')
