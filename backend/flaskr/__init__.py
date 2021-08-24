from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from models import setup_db, Question, Category, db

ITEMS_PER_PAGE = 10


def get_paginated_items(request, items, items_per_page=ITEMS_PER_PAGE):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in items]
    current_items = items[start:end]
    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resource={r'*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                                'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                                'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    Returns all categories
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            return jsonify({
                'success': True,
                'categories': {category.id: category.type for category in categories},
            })
        except:
            abort(500)

    '''
    Returns paginated questions (10 questions per page)
    '''
    @app.route('/questions', methods=['GET'])
    def get_quetsions():
        try:
            questions = get_paginated_items(request, Question.query.all())
            categories = Category.query.all()
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(Question.query.all()),
                'categories': {category.id: category.type for category in categories},
                'current_category': None
            })
        except:
            abort(500)

    '''
    Returns specific question by ID
    '''
    @app.route('/questions/<question_id>', methods=['GET'])
    def get_question(question_id):
        try:
            question = Question.query.get(question_id)

            return jsonify({
                'success': True,
                'question': question.format(),
                'total_questions': len(Question.query.all())
            })
        except:
            if question == None:
                abort(404)
            else:
                abort(500)

    '''
    Deletes a question by ID
    '''
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            question.delete()
            db.session.commit()
            return jsonify({
                'success': True,
                'deleted_question_id': question_id,
                'total_questions': len(Question.query.all())
            })
        except:
            db.session.rollback()
            if question == None:
                abort(404)
            else:
                abort(500)
        finally:
            db.session.close()

    '''
    Adds a new question or searches for questions based on search term
    '''
    @app.route('/questions', methods=['POST'])
    def post_or_search_question():
        try:
            res = request.get_json()
            search_term = res.get('searchTerm', None)
            if search_term != None:
                questions = db.session.query(Question).filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                questions = get_paginated_items(request, questions)
                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': len(Question.query.all()),
                    'current_category': None
                })

            new_question = Question(
                question=res.get('question', None),
                answer=res.get('answer', None),
                category=res.get('category', None),
                difficulty=res.get('difficulty', None)
            )
            db.session.add(new_question)
            db.session.commit()
            return jsonify({
                'success': True,
                'total_questions': len(Question.query.all())
            })
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    '''
    Returns paginated questions based on the selected category
    '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_quetsions_by_category(category_id):
        try:
            current_category = Category.query.get(category_id)
            questions = get_paginated_items(
                request,
                db.session.query(Question)
                .filter(Question.category == category_id)
                .all())

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(Question.query.all()),
                'current_category': current_category.format()
            })
        except:
            if current_category == None:
                abort(404)
            else:
                abort(500)

    '''
    Plays trivia quiz by returning a new random question that 
    haven't been asked before based on the category of the quiz
    '''
    @app.route('/quizzes', methods=['POST'])
    def post_quizzes():
        try:
            res = request.get_json()
            category_ids = [id[0] for id in db.session.query(Category.id).all()]  
            questions = []
            res.get('quiz_category', None)['id'] = int(res.get('quiz_category', None)['id'])
            
            if res.get('quiz_category', None)['id'] == 0:
                questions = Question.query.filter(
                    Question.id.notin_(res.get('previous_questions'))).all()
            elif res.get('quiz_category', None)['id'] in category_ids:
                questions = Question.query.filter_by(category=res.get('quiz_category', None)[
                    'id']).filter(Question.id.notin_(res.get('previous_questions'))).all()
            else:
                raise Exception

            question = random.choice(questions) if questions else None
            response_body = {'success': True}
            if question != None:
                response_body['question'] = question.format()

            return jsonify(response_body)
        except:
            if 'quiz_category' not in res or 'previous_questions' not in res:
                abort(422)
            elif res.get('quiz_category', None)['id'] not in category_ids:
                abort(400)
            else:
                abort(500)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {"success": False,
                    "error": 404,
                    "message": "resource not found"
                }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False,
                    "error": 422,
                    "message": "unprocessable"
                }),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {"success": False,
                    "error": 400,
                    "message":
                    "bad request"
                }),
            400,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {"success": False,
                    "error": 405,
                    "message": "method not allowed"
                }),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False,
                    "error": 500,
                    "message": "internal server error"
                }),
            405,
        )
    return app

if __name__ == '__main__':
    create_app()
