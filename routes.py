""" Defines application routes """

from middleware import candidates
from middleware import candidate_by_id
from middleware import add_candidate
from middleware import update_candidate_name
from middleware import random_candidates
from middleware import delete_candidate
from middleware import random_projects
from middleware import add_project

from flask import jsonify
from flask import render_template
from flask import flash
from flask import abort


def init_api_routes(app):
    """ Adds API routes to Flask app """
    if app:
        app.add_url_rule('/api/candidates/<string:id>',
                         'candidate_by_id', candidate_by_id, methods=['GET'])
        app.add_url_rule('/api/candidates', 'candidates',
                         candidates, methods=['GET'])
        app.add_url_rule('/api/candidates', 'add_candidate',
                         add_candidate, methods=['POST'])
        app.add_url_rule('/api/candidates/<string:id>/name/<string:new_name>',
                         'update_candidate_name', update_candidate_name, methods=['PUT'])
        app.add_url_rule('/api/candidates/random', 'get_random_candidate',
                         random_candidates, methods=['GET'], defaults={'number_of_items': 1})
        app.add_url_rule('/api/candidates/random/<int:number_of_items>',
                         'get_random_candidates', random_candidates, methods=['GET'])
        app.add_url_rule('/api/candidates/delete/<string:id>',
                         'delete_candidate', delete_candidate, methods=['DELETE'])
        app.add_url_rule('/api/projects/random/<int:number_of_items>',
                         'get_random_projects', random_projects, methods=['GET'])
        app.add_url_rule('/api/projects', 'add_project',
                         add_project, methods=['POST'])
        app.add_url_rule('/api/list_routes', 'list_routes',
                         list_routes, methods=['GET'], defaults={'app': app})


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
    return render_template('about.html', selected_menu_item='about')


def page_project():
    """ Renders project page """
    return render_template('project.html', selected_menu_item='project')


def page_experience():
    """ Renders candidate experience """
    return render_template('experience.html', selected_menu_item='experience')


def page_candidate():
    """ Renders candidate info """
    current_candidates = candidates(serialize=False)
    return render_template(
        'candidate.html',
        selected_menu_item='candidate',
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
        app.add_url_rule('/project', 'page_project',
                         page_project, methods=['GET'])
        app.add_url_rule('/candidate', 'page_candidate',
                         page_candidate, methods=['GET'])
        app.add_url_rule('/experience', 'page_experience',
                         page_experience, methods=['GET'])
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
