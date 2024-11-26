from app.extensions import db
class ClassRoom(db.Model):
    __tablename__ = 'class_rooms'

    id = db.Column(db.Integer, primary_key=True)
    id_class_room = db.Column(db.Integer, nullable=False)
    name_class = db.Column(db.String(255), nullable=False)
    class_field = db.Column(db.String(255))  # 'class' là từ khóa trong Python, đổi thành 'class_field'
    slug = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Relationships
    posts = db.relationship('Post', back_populates='class_room')
