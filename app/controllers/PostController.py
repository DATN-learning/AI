from flask import request, jsonify
from app.models.post import Post
from app.models.image import Image  # Import model liên quan đến hình ảnh
from app.extensions import db

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_similar_posts(description, posts, cosine, top = 5):
    recommended_posts = []
    post_index = 0
    for post in posts:
        if post['description'] == description:
            post_index = posts.index(post)
            break
    similar_scores = list(enumerate(cosine[post_index]))
    similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
    similar_scores = similar_scores[1:top+1]
    for score in similar_scores:
        recommended_posts.append(posts[score[0]])
    return recommended_posts
    
    
def post_content():
    # Lấy dữ liệu từ request
    description = request.json.get('description')
    class_room_id = request.json.get('class_room_id')
    subject_id = request.json.get('subject_id')

    # Kiểm tra dữ liệu đầu vào
    if not description:
        errors = {'description': ['Description is required']}
        return jsonify({'status': False, 'message': 'Validation error', 'error': errors}), 400

    if not class_room_id or not subject_id:
        errors = {'class_room_id': 'Classroom ID and Subject ID are required'}
        return jsonify({'status': False, 'message': 'Validation error', 'error': errors}), 400

    # Tạo một đối tượng giả lập request.json để truyền dữ liệu
    fake_request_json = {'class_room_id': class_room_id, 'subject_id': subject_id}

    # Gọi hàm get_post_question_by_classroom() với dữ liệu giả lập
    response, status_code = get_post_question_by_classroom(fake_request_json)
    if not response['status']:
        return jsonify(response), status_code
    
    # Trả về dữ liệu JSON
    return jsonify({
        'status': True,
        'message': 'Post content and related posts retrieved successfully',
        'description': description,
        'related_posts': response['data']
    }), 200


# Hàm get_post_question_by_classroom được sửa đổi để nhận tham số data thay vì dùng trực tiếp request.json
def get_post_question_by_classroom(data):
    # Kiểm tra dữ liệu đầu vào
    class_room_id = data.get('class_room_id')
    subject_id = data.get('subject_id')

    errors = {}
    if not class_room_id:
        errors['class_room_id'] = ['Classroom ID is required']
    if not subject_id:
        errors['subject_id'] = ['Subject ID is required']
    if errors:
        return {'status': False, 'message': 'Validation error', 'error': errors}, 400

    # Truy vấn dữ liệu từ bảng Post
    if subject_id:
        posts = Post.query.filter_by(class_room_id=class_room_id, subject_id=subject_id).all()
    else:
        posts = Post.query.filter_by(class_room_id=class_room_id).all()

    # Xử lý dữ liệu bài đăng
    results = []
    for post in posts:
        # Lấy danh sách hình ảnh liên quan
        images = Image.query.filter_by(id_query_image=post.id_post).all()
        image_data = [{'id': image.id, 'url_image': f"/images/{image.url_image}"} for image in images]

        # Gộp dữ liệu phân tích nếu có
        analytics = post.analytics  # Quan hệ back_populates
        if analytics:
            combined_analytics = " ".join(a.text_data for a in analytics)  # Gộp các chuỗi `text_data` thành 1 chuỗi
        else:
            combined_analytics = ""  # Nếu không có dữ liệu phân tích, trả về chuỗi rỗng

        
        # Cấu trúc dữ liệu trả về
        post_data = {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'category_post': post.category_post,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'images': image_data,
            'analytics': combined_analytics  # Thay thế danh sách bằng chuỗi gộp
        }
        results.append(post_data)

    descriptions = [result['analytics'] for result in results]
    tfidf = TfidfVectorizer().fit_transform(descriptions)

    # Chuyển đổi csr_matrix thành danh sách để trả về JSON
    #tfidf_array = tfidf.tolist()  # Hoặc sử dụng .tolist()
    cosine_sim = cosine_similarity(tfidf, tfidf)
    cosine_sim_list = cosine_sim.tolist()
    recommended_posts = recommend_similar_posts(1, results, cosine_sim_list)

    # Trả về dữ liệu JSON
    return {'status': True, 'message': 'Posts retrieved successfully', 'data': recommended_posts}, 200

