from flask import Blueprint
from app.controllers.ChapterController import get_chapter_subject
from app.controllers.PostController import get_post_question_by_classroom
from app.controllers.PostController import post_content
chapter_bp = Blueprint('chapter', __name__)

chapter_bp.route('/classroom/getChapterSubject', methods=['POST'])(get_chapter_subject)

post = Blueprint('post', __name__)

post.route('/manapost/getPostQuestionByClassroom', methods=['POST'])(get_post_question_by_classroom)

content = Blueprint('content', __name__)
post.route('/manapost/getcontent', methods=['POST'])(post_content)
