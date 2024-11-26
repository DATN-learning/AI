from flask import request, jsonify
from app.models.chapter_subject import ChapterSubject
from app.models.subject import Subject
from app.models.lesstion_chapter import LesstionChapter
from app.extensions import db

def get_chapter_subject():
    subject_id = request.json.get('subject_id')
    
    if not subject_id:
        return jsonify({'error': {'subject_id': ['Subject ID is required']}}), 400
    
    subject = Subject.query.filter_by(id=subject_id).first()
    if not subject:
        return jsonify({
            'status': False,
            'message': 'subject not found',
            'data': {'chapter': None}
        }), 200
    
    chapters = ChapterSubject.query.filter_by(subject_id=subject.id).all()
    result = []
    for chapter in chapters:
        chapter_data = {
            'id': chapter.id,
            'name_chapter_subject': chapter.name_chapter_subject,
            'chapter_image': f"/images/{chapter.chapter_image}" if chapter.chapter_image else None,
            'lessions': [{'id': l.id, 'name': l.name_lesstion_chapter} for l in chapter.lessions]
        }
        result.append(chapter_data)
    
    return jsonify({
        'status': True,
        'message': 'chapter found',
        'data': {'chapter': result}
    }), 200
