from app.extensions import db

class LesstionChapter(db.Model):
    __tablename__ = 'lesstion_chapters'

    id = db.Column(db.Integer, primary_key=True)
    id_lesstion_chapter = db.Column(db.Integer, nullable=False)
    chapter_subject_id = db.Column(db.Integer, db.ForeignKey('chapter_subjects.id'), nullable=False)
    name_lesstion_chapter = db.Column(db.String(255), nullable=False)
    description_lesstion_chapter = db.Column(db.Text)
    number_lesstion_chapter = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    chapter = db.relationship('ChapterSubject', back_populates='lessions')
