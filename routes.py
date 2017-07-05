""" Defines application routes """

from decorators import authenticate

from middleware import candidates
from middleware import candidate_by_id
from middleware import add_candidate
from middleware import update_candidate
from middleware import delete_candidate
from middleware import initialize_database as init_db
from middleware import fill_database as fill_db
from middleware import build_message

from flask import jsonify
from flask import render_template
from flask import make_response
from flask import flash
from flask import current_app
from flask import abort

TOKEN_HEADER_NAME = "MY_AUTH_TOKEN"


def init_api_routes(app):
    """ Adds API routes to Flask app """
    if app:
        app.add_url_rule('/api/candidates/<string:candidate_id>',
                         'candidate_by_id', candidate_by_id, methods=['GET'])
        app.add_url_rule('/api/candidates', 'candidates',
                         candidates, methods=['GET'])
        app.add_url_rule('/api/candidates', 'add_candidate',
                         add_candidate, methods=['POST'])
        app.add_url_rule('/api/candidates/<string:candidate_id>',
                         'update_candidate', update_candidate, methods=['PUT'])
        app.add_url_rule('/api/candidates/<string:candidate_id>',
                         'delete_candidate', delete_candidate, methods=['DELETE'])
        app.add_url_rule('/api/list_routes', 'list_routes',
                         list_routes, methods=['GET'], defaults={'app': app})
        app.add_url_rule('/api/initdb', 'initdb', initialize_database)
        app.add_url_rule('/api/filldb', 'filldb', fill_database)


def list_routes(app):
    """ Lists all API routes """
    result = []

    for route in app.url_map.iter_rules():
        result.append({
            "methods": list(route.methods),
            "route": str(route)
        })

    return jsonify({"routes": result, "total": len(result)})


def page_about():
    """ Renders about page """
    response = make_response(render_template(
        'about.html', selected_menu_item="about"))
    return response


def page_candidates():
    """ Renders candidate info """
    current_candidates = candidates(serialize=False)
    return render_template(
        'candidate.html',
        selected_menu_item='candidates',
        candidates=current_candidates)


def page_index():
    """ Renders index page """
    return render_template('index.html', selected_menu_item='index')


def init_website_routes(app):
    """ Adds website routes to Flask app """
    if app:
        app.add_url_rule('/crash', 'crash_server',
                         crash_server, methods=['GET'])
        app.add_url_rule('/about', 'page_about', page_about, methods=['GET'])
        app.add_url_rule('/candidates', 'page_candidates',
                         page_candidates, methods=['GET'])
        app.add_url_rule('/', 'page_index', page_index, methods=['GET'])


def crash_server():
    """ Triggers an error 500 """
    abort(500)


def handle_error_404(error):
    """ Handles 404 errors """

    flash('Server says: {}'.format(error), 'error')
    return render_template('404.html', selected_menu_item=None)


def handle_error_500(error):
    """ Handles 500 errors """
    flash('Server says: {}'.format(error), 'error')
    return render_template('500.html', selected_menu_item=None)


def init_error_handlers(app):
    """ Defines error handlers """
    if app:
        app.register_error_handler(404, handle_error_404)
        app.register_error_handler(500, handle_error_500)


def initialize_database():
    """ Initializes database """
    message_key = "Initialize database"

    try:
        init_db()
    except ValueError as err:
        return jsonify(build_message(message_key, err.message))

    return jsonify(build_message(message_key, "OK"))


def fill_database():
    """ Fills database """
    message_key = "Fill database"

    try:
        fill_db()
    except ValueError as err:
        return jsonify(build_message(message_key, str(err)))

    return jsonify(build_message(message_key, "OK"))
