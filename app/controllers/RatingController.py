from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.ratings import Rating
from app.models.user import User
from app.models.lesstion_chapter import LesstionChapter
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
        # Lấy user_id từ query parameters
        user_id = request.args.get('user_id')

        # Kiểm tra đầu vào
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

    
def getRating():
    try:
        all_ratings_response = get_all_ratings()
        all_ratings_data = all_ratings_response[0].get_json()

        print("Status (all ratings):", all_ratings_data['status'])
        print("Message (all ratings):", all_ratings_data['message'])
        print("Data (all ratings):", all_ratings_data['data'])

        user_id = request.args.get('user_id', None)

        if not user_id:
            return jsonify({
                'status': False,
                'message': 'Validation error',
                'error': {'user_id': 'This field is required in query parameters'}
            }), 400

        lessons_response = get_lessons_by_user_ratings()
        lessons_data = lessons_response[0].get_json()

        print("User ID:", user_id)
        print("Status (user ratings):", lessons_data['status'])
        print("Message (user ratings):", lessons_data['message'])
        print("Data (user ratings):", lessons_data['data'])

        return jsonify({
            'status': True,
            'ratings': all_ratings_data['data'],
            'lessons': lessons_data['data']
        }), 200
    except Exception as e:
        # Xử lý lỗi và ghi log
        print(f"Error in getRating: {str(e)}")
        return jsonify({
            'status': False,
            'message': 'Error retrieving data',
            'error': str(e)
        }), 500
    
import pandas as pd
import numpy as np
from flask import jsonify
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

def create_matrix(df):
    N = df['user_id'].nunique()
    M = df['lesstion_chapter_id'].nunique()

    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N))))
    story_mapper = dict(zip(np.unique(df["lesstion_chapter_id"]), list(range(M))))

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["user_id"])))
    story_inv_mapper = dict(zip(list(range(M)), np.unique(df["lesstion_chapter_id"])))

    user_index = [user_mapper[i] for i in df['user_id']]
    story_index = [story_mapper[i] for i in df['lesstion_chapter_id']]

    X = csr_matrix((df["rating"], (story_index, user_index)), shape=(M, N))

    return X, user_mapper, story_mapper, user_inv_mapper, story_inv_mapper


# @story_controller.route('/stories-user/<userId>', methods=['GET'])
# @cross_origin(origin='*', headers=['Content-Type'])
def get_stories(userId):
    stories = get_lessons_by_user_ratings()
    ratings = get_all_ratings()
    
    # Convert stories and ratings to DataFrames
    stories_df = pd.DataFrame(stories)
    ratings_df = pd.DataFrame(ratings)

    all_ratings_data = ratings[0].get_json()
    print("Data (all ratings):", all_ratings_data['data'])
    
    n_ratings = len(ratings_df)
    n_stories = len(stories_df)
    n_users = len(set(ratings_df['user_id']))

    print(f"Number of ratings: {n_ratings}")
    print(f"Number of unique movieId's: {n_stories}")
    print(f"Number of unique users: {n_users}")
    print(f"Average ratings per user: {round(n_ratings/n_users, 2)}")
    print(f"Average ratings per movie: {round(n_ratings/n_stories, 2)}")
    
    user_freq = ratings_df[['user_id', 'lesstion_chapter_id']].groupby('user_id').count().reset_index()
    user_freq.columns = ['user_id', 'n_ratings']
    print(user_freq.head())  

    mean_rating = ratings_df[['lesstion_chapter_id', 'rating']].groupby('lesstion_chapter_id').mean()

    lowest_rated = mean_rating['rating'].idxmin()
    stories_df.loc[stories_df['id'] == lowest_rated]

    highest_rated = mean_rating['rating'].idxmax()
    stories_df.loc[stories_df['id'] == highest_rated]

    # show number of people who rated movies rated movie highest
    ratings_df[ratings_df['lesstion_chapter_id']==highest_rated]
    # show number of people who rated movies rated movie lowest
    ratings_df[ratings_df['lesstion_chapter_id']==lowest_rated]

    movie_stats = ratings_df.groupby('lesstion_chapter_id')[['rating']].agg(['count', 'mean'])
    movie_stats.columns = movie_stats.columns.droplevel()

    X, user_mapper, story_mapper, user_inv_mapper, story_inv_mapper = create_matrix(ratings_df)

    def find_similar_movies(movie_id, X, k, metric='cosine', show_distance=False):
    
        neighbour_ids = []
        
        movie_ind = story_mapper[movie_id]
        movie_vec = X[movie_ind]
        k+=1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
        kNN.fit(X)
        movie_vec = movie_vec.reshape(1,-1)
        neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)
        for i in range(0,k):
            n = neighbour.item(i)
            neighbour_ids.append(story_inv_mapper[n])
        neighbour_ids.pop(0)
        return neighbour_ids

    def recommend_movies_for_user(user_id, X, user_mapper, movie_mapper, movie_inv_mapper, k=10):
        df1 = ratings_df[ratings_df['user_id'] == user_id]
        
        if df1.empty:
            print(f"User with ID {user_id} does not exist.")
            return []

        movie_id = df1[df1['rating'] == max(df1['rating'])]['lesstion_chapter_id'].iloc[0]

        movie_titles = dict(zip(stories_df['id'], stories_df['title']))

        similar_ids = find_similar_movies(movie_id, X, k)
        movie_title = movie_titles.get(movie_id, "Movie not found")

        if movie_title == "Movie not found":
            print(f"Movie with ID {movie_id} not found.")
            return []

        print(f"Since you watched {movie_title}, you might also like:")
        for i in similar_ids:
            print(movie_titles.get(i, "Movie not found"))
        return similar_ids
    
    user_id = userId
    listId =  recommend_movies_for_user(user_id, X, user_mapper, story_mapper, story_inv_mapper, k=10)

    return jsonify(listId)