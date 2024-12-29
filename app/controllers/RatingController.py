from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.ratings import Rating
from app.models.user import User
from app.models.lesstion_chapter import LesstionChapter
from app.models.chapter_subject import ChapterSubject 
import pandas as pd
import numpy as np
from flask import jsonify
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

def get_all_ratings():
    try:
        ratings = Rating.query.all()
        result = []
        for rating in ratings:
            result.append({
                'id': rating.id,
                'rating_id': rating.rating_id,
                'user_id': rating.user_id,
                'lesstion_chapter_id': rating.lesstion_chapter_id,
                'content': rating.content,
                'rating': rating.rating,
                'created_at': rating.created_at.isoformat() if rating.created_at else None,
                'updated_at': rating.updated_at.isoformat() if rating.updated_at else None
            })

        return jsonify({
            'status': True,
            'message': 'Get all ratings success',
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'status': False,
            'message': 'Error retrieving all ratings',
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
                'lesstion_chapter_id': rating.lesstion_chapter_id,
                'lesson_chapter_name': rating.lesson_chapter.name_lesstion_chapter if rating.lesson_chapter else None,
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
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({
                'status': False,
                'message': 'Validation error',
                'error': {'user_id': 'This field is required'}
            }), 400

        ratings = Rating.query.filter(Rating.user_id == user_id)\
            .join(LesstionChapter, LesstionChapter.id == Rating.lesstion_chapter_id)\
            .all()
        
        result = []
        for rating in ratings:
            result.append({
                'user_id': rating.user_id,
                "lesstion_chapter_id": rating.lesson_chapter.id if rating.lesson_chapter else None,
                "name_lesstion_chapter": rating.lesson_chapter.name_lesstion_chapter if rating.lesson_chapter else None,
            })

        return jsonify({
            'status': True,
            'message': 'Get lessons rated by user success',
            'data': result
        }), 200
    except Exception as e:
        print(f"Error in get_lessons_by_user_ratings: {str(e)}")
        return jsonify({
            'status': False,
            'message': 'Error retrieving lessons',
            'error': str(e)
        }), 500

    
import pandas as pd
import numpy as np
from flask import jsonify
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

def get_lesson_by_id(lesson_id):
    try:
        lesson_id = int(lesson_id)
        return LesstionChapter.query.filter(LesstionChapter.id == lesson_id).first()
    except Exception as e:
        print(f"Error retrieving lesson {lesson_id}: {str(e)}")
        return None

def create_rating_matrix(ratings_df):
    ratings_df['user_id'] = ratings_df['user_id'].astype('int32')
    ratings_df['lesstion_chapter_id'] = ratings_df['lesstion_chapter_id'].astype('int32')
    ratings_df['rating'] = ratings_df['rating'].astype('float32')
    
    N = ratings_df['user_id'].nunique()
    M = ratings_df['lesstion_chapter_id'].nunique()

    user_mapper = {int(id_): idx for idx, id_ in enumerate(ratings_df['user_id'].unique())}
    lesson_mapper = {int(id_): idx for idx, id_ in enumerate(ratings_df['lesstion_chapter_id'].unique())}
    
    user_inv_mapper = {idx: int(id_) for id_, idx in user_mapper.items()}
    lesson_inv_mapper = {idx: int(id_) for id_, idx in lesson_mapper.items()}

    user_index = [user_mapper[int(i)] for i in ratings_df['user_id']]
    lesson_index = [lesson_mapper[int(i)] for i in ratings_df['lesstion_chapter_id']]

    X = csr_matrix((ratings_df["rating"], (lesson_index, user_index)), shape=(M, N))
    
    return X, user_mapper, lesson_mapper, user_inv_mapper, lesson_inv_mapper

def find_similar_lessons(lesson_id, X, lesson_mapper, lesson_inv_mapper, k=10):
    try:
        lesson_id = int(lesson_id)
        lesson_idx = lesson_mapper[lesson_id]
        lesson_vec = X[lesson_idx]
        
        kNN = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric='cosine')
        kNN.fit(X)
        
        distances, indices = kNN.kneighbors(lesson_vec.reshape(1, -1))
        similar_lessons = [int(lesson_inv_mapper[idx]) for idx in indices.flatten()[1:]]
        
        return similar_lessons
    except Exception as e:
        print(f"Error in find_similar_lessons: {str(e)}")
        return []

def get_lesson_recommendations(user_id):
    try:
        user_id = int(user_id)
        
        ratings = get_all_ratings()
        all_ratings_data = ratings[0].get_json()

        ratings_data = []
        for r in all_ratings_data['data']:
            try:
                ratings_data.append({
                    'user_id': int(r['user_id']),
                    'lesstion_chapter_id': int(r['lesstion_chapter_id']),
                    'rating': float(r['rating'])
                })
            except (ValueError, TypeError) as e:
                print(f"Error converting rating data: {str(e)}")
                continue

        ratings_df = pd.DataFrame(ratings_data)
        
        if ratings_df.empty:
            return jsonify({
                'status': False,
                'message': 'No valid ratings data available',
                'recommendations': []
            }), 404

        user_ratings = ratings_df[ratings_df['user_id'] == user_id]
        if user_ratings.empty:
            return jsonify({
                'status': False,
                'message': f'No ratings found for user {user_id}',
                'recommendations': []
            }), 404

        X, user_mapper, lesson_mapper, user_inv_mapper, lesson_inv_mapper = create_rating_matrix(ratings_df)
        top_rated_lesson = int(user_ratings.loc[user_ratings['rating'].idxmax()]['lesstion_chapter_id'])
        similar_lessons = find_similar_lessons(top_rated_lesson, X, lesson_mapper, lesson_inv_mapper)

        recommended_lessons = []
        for lesson_id in similar_lessons:
            lesson = get_lesson_by_id(lesson_id)
            if lesson:
                # Directly fetch chapter using chapter_subject_id
                chapter = ChapterSubject.query.filter(ChapterSubject.id == lesson.chapter_subject_id).first()
                
                if chapter:
                    recommended_lessons.append({
                        'chapter': {
                            'id': int(chapter.id),
                            'id_chapter_subject': str(chapter.id_chapter_subject),
                            'subject_id': int(chapter.subject_id),
                            'name_chapter_subject': str(chapter.name_chapter_subject),
                            'chapter_image': f'http://192.168.1.125:8000/images/{chapter.chapter_image}' if chapter.chapter_image else None,
                        },
                        'lesson': {
                            'id': int(lesson.id),
                            'name_lesstion_chapter': str(lesson.name_lesstion_chapter),
                            'similarity_score': float(similar_lessons.index(lesson_id) / len(similar_lessons)),
                            'description_lesstion_chapter': str(lesson.description_lesstion_chapter),
                        }
                    })

        return jsonify({
            'recommendations': recommended_lessons
        }), 200

    except Exception as e:
        print(f"Error in get_lesson_recommendations: {str(e)}")
        return jsonify({
            'status': False,
            'message': 'Error generating recommendations',
            'error': str(e),
            'error_type': str(type(e))
        }), 500
