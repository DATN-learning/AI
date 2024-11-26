from app.extensions import db

class ChapterSubject(db.Model):
    __tablename__ = 'chapter_subjects'

    id = db.Column(db.Integer, primary_key=True)
    id_chapter_subject = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    name_chapter_subject = db.Column(db.String(255), nullable=False)
    chapter_image = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    number_chapter = db.Column(db.Integer)

    subject = db.relationship('Subject', back_populates='chapters')
    lessions = db.relationship('LesstionChapter', back_populates='chapter')
