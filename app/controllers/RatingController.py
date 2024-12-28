from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.ratings import Rating
from app.models.user import User
from app.models.lesstion_chapter import LesstionChapter


def get_all_ratings():
    try:
        ratings = db.session.query(Rating).join(User, Rating.user_id == User.id).join(LesstionChapter, Rating.lesstion_chapter_id == LesstionChapter.id).all()
        result = []
        for rating in ratings:
            result.append({
                'id': rating.id,
                'rating_id': rating.rating_id,
                'user_id': rating.user_id,
                'user_name': f"{rating.user.first_name} {rating.user.last_name}" if rating.user else None,
                'lesson_chapter_id': rating.lesstion_chapter_id,
                'lesson_chapter_name': rating.lesson_chapter.name_lesstion_chapter if rating.lesson_chapter else None,
                'content': rating.content,
                'rating': rating.rating,
                'created_at': rating.created_at,
                'updated_at': rating.updated_at
            })
        return jsonify({
            'status': True,
            'message': 'Get all ratings success',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Error retrieving ratings',
            'error': str(e)
        }), 500


def get_rating_by_lesson_chapter_id():
    try:
        # Lấy ID từ request JSON
        data = request.get_json()
        lesstion_chapter_id = data.get('lesstion_chapter_id')

        # Kiểm tra đầu vào
        if not lesstion_chapter_id:
            return jsonify({
                'status': False,
                'message': 'Validation error',
                'error': {'lesstion_chapter_id': 'This field is required'}
            }), 400

        ratings = (
            Rating.query
            .filter(Rating.lesstion_chapter_id == lesstion_chapter_id)
            .join(User, User.id == Rating.user_id)
            .join(LesstionChapter, LesstionChapter.id == Rating.lesstion_chapter_id)
            .all()
        )

        # Chuẩn bị kết quả
        result = []
        for rating in ratings:
            result.append({
                'id': rating.id,
                'rating_id': rating.rating_id,
                'user_id': rating.user_id,
                'user_name': f"{rating.user.first_name} {rating.user.last_name}" if rating.user else None,
                'lesstion_chapter_id': rating.lesstion_chapter_id,
                'lesson_chapter_name': rating.lesson_chapter.name_lesstion_chapter if rating.lesson_chapter else None,
                'content': rating.content,
                'rating': rating.rating,
                'created_at': rating.created_at,
                'updated_at': rating.updated_at
            })

        return jsonify({
            'status': True,
            'message': 'Get ratings by lesson chapter ID success',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Error retrieving ratings',
            'error': str(e)
        }), 500
    
def get_lessons_by_user_ratings():
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        # Kiểm tra đầu vào
        if not user_id:
            return jsonify({
                'status': False,
                'message': 'Validation error',
                'error': {'user_id': 'This field is required'}
            }), 400

        ratings = (
            Rating.query
            .filter(Rating.user_id == user_id)
            .join(LesstionChapter, LesstionChapter.id == Rating.lesstion_chapter_id)
            .all()
        )

        result = []
        for rating in ratings:
            result.append({
                "lesstion_chapter_id": rating.lesson_chapter.id,
                "name_lesstion_chapter": rating.lesson_chapter.name_lesstion_chapter,
                "description_lesstion_chapter": rating.lesson_chapter.description_lesstion_chapter,
                "number_lesstion_chapter": rating.lesson_chapter.number_lesstion_chapter,
                "rating_id": rating.id,
                "rating_content": rating.content,
                "rating_score": rating.rating,
                "created_at": rating.created_at.isoformat(),
                "updated_at": rating.updated_at.isoformat()
            })

        return jsonify({
            'status': True,
            'message': 'Get lessons rated by user success',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Error retrieving lessons',
            'error': str(e)
        }), 500
