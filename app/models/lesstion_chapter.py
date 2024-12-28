from app.extensions import db

class LesstionChapter(db.Model):
    __tablename__ = 'lesstion_chapters'

    id = db.Column(db.BigInteger, primary_key=True)
    id_lesstion_chapter = db.Column(db.BigInteger, nullable=False)
    chapter_subject_id = db.Column(db.BigInteger, db.ForeignKey('chapter_subjects.id'), nullable=False)
    name_lesstion_chapter = db.Column(db.String(255), nullable=False)
    description_lesstion_chapter = db.Column(db.Text)
    number_lesstion_chapter = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Define relationships
    ratings = db.relationship('Rating', back_populates='lesson_chapter', lazy='dynamic')
    chapter = db.relationship('ChapterSubject', back_populates='lessions')