"""
CodeCraftHub - Personalized Learning Platform API
A Flask REST API for developers to manage and track courses they want to learn.
Data is stored locally in courses.json without requiring an external database.
"""

from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Configuration: file path where courses data is stored
DATA_FILE = 'courses.json'
VALID_STATUSES = ['Not Started', 'In Progress', 'Completed']


# ==============================================================================
# Helper Functions for JSON Data Persistence
# ==============================================================================

def load_courses():
    """
    Load courses list from the JSON file.
    If the file does not exist, it initializes an empty JSON array and returns [].
    """
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
            return []
        except IOError as e:
            app.logger.error(f"Error creating {DATA_FILE}: {e}")
            return []

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        app.logger.error(f"Error reading {DATA_FILE}: {e}")
        return []


def save_courses(courses):
    """
    Save the list of courses back to the JSON file with indentation.
    Returns True if successful, False otherwise.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(courses, f, indent=2)
        return True
    except IOError as e:
        app.logger.error(f"Error saving to {DATA_FILE}: {e}")
        return False


def get_next_id(courses):
    """
    Generate the next unique integer ID for a new course.
    Starts at 1 if the list is empty.
    """
    if not courses:
        return 1
    return max(course['id'] for course in courses) + 1


# ==============================================================================
# CORS Support for Frontend & Live Server
# ==============================================================================

@app.after_request
def add_cors_headers(response):
    """Allow Cross-Origin requests so the frontend can run on Live Server or any port."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response


@app.route('/api/courses', methods=['OPTIONS'])
@app.route('/api/courses/<path:subpath>', methods=['OPTIONS'])
def options_handler(subpath=None):
    """Handle CORS preflight requests."""
    return ('', 204)


# ==============================================================================
# Root & Information Endpoint
# ==============================================================================

@app.route('/', methods=['GET'])
def index():
    """
    Serve either the frontend dashboard (if accessed via browser)
    or the JSON API directory (if accessed by API clients/tests).
    """
    accept_header = request.headers.get('Accept', '')
    if 'text/html' in accept_header and os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}

    return jsonify({
        'success': True,
        'message': 'Welcome to CodeCraftHub Learning Management System API',
        'endpoints': {
            'GET /api/courses': 'List all courses',
            'GET /api/courses/<id>': 'Get details of a specific course',
            'POST /api/courses': 'Add a new course',
            'PUT /api/courses/<id>': 'Update an existing course',
            'DELETE /api/courses/<id>': 'Delete a course',
            'GET /api/courses/stats': 'Get course statistics (bonus)',
            'GET /api/courses/search?q=<term>': 'Search courses by keyword (bonus)',
            'GET /dashboard': 'Interactive Web Dashboard'
        }
    }), 200


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Direct route to access the CodeCraftHub web dashboard."""
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    return jsonify({'success': False, 'error': 'Dashboard index.html not found'}), 404



# ==============================================================================
# REST API Endpoints for Course Management
# ==============================================================================

@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    """
    Retrieve all courses stored in CodeCraftHub.
    Returns:
        JSON response with count and list of courses.
    """
    courses = load_courses()
    return jsonify({
        'success': True,
        'count': len(courses),
        'courses': courses
    }), 200


@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """
    Retrieve a specific course by its integer ID.
    Args:
        course_id: The ID of the course to retrieve.
    Returns:
        JSON with the course data or 404 error if not found.
    """
    courses = load_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    if course:
        return jsonify({
            'success': True,
            'course': course
        }), 200
    return jsonify({
        'success': False,
        'error': 'Course not found'
    }), 404


@app.route('/api/courses', methods=['POST'])
def add_course():
    """
    Add a new course to CodeCraftHub.
    Expected JSON Body:
        name (str): Course title (required)
        description (str): Course description (required)
        target_date (str): Format YYYY-MM-DD (required)
        status (str): "Not Started" | "In Progress" | "Completed" (required)
    Returns:
        201 Created on success, 400 Bad Request on validation failure.
    """
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({
            'success': False,
            'error': 'Invalid request body. Expected JSON object.'
        }), 400

    # Validate required fields
    required_fields = ['name', 'description', 'target_date', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400

    # Validate status value
    if data['status'] not in VALID_STATUSES:
        return jsonify({
            'success': False,
            'error': f"Status must be one of: {', '.join(VALID_STATUSES)}"
        }), 400

    courses = load_courses()
    new_course = {
        'id': get_next_id(courses),
        'name': data['name'],
        'description': data['description'],
        'target_date': data['target_date'],
        'status': data['status'],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    courses.append(new_course)
    if not save_courses(courses):
        return jsonify({
            'success': False,
            'error': 'Failed to save course to data store'
        }), 500

    return jsonify({
        'success': True,
        'message': 'Course added successfully',
        'course': new_course
    }), 201


@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    Update an existing course by its ID.
    Args:
        course_id: The ID of the course to update.
    Expected JSON Body:
        Optional fields to update: name, description, target_date, status.
    Returns:
        200 OK on success, 400 on invalid input, 404 if not found.
    """
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({
            'success': False,
            'error': 'Invalid request body. Expected JSON object.'
        }), 400

    courses = load_courses()
    course_index = next((i for i, c in enumerate(courses) if c['id'] == course_id), None)
    if course_index is None:
        return jsonify({
            'success': False,
            'error': 'Course not found'
        }), 404

    # Validate status if provided
    if 'status' in data and data['status'] not in VALID_STATUSES:
        return jsonify({
            'success': False,
            'error': f"Status must be one of: {', '.join(VALID_STATUSES)}"
        }), 400

    course = courses[course_index]
    if 'name' in data:
        course['name'] = data['name']
    if 'description' in data:
        course['description'] = data['description']
    if 'target_date' in data:
        course['target_date'] = data['target_date']
    if 'status' in data:
        course['status'] = data['status']

    if not save_courses(courses):
        return jsonify({
            'success': False,
            'error': 'Failed to update course in data store'
        }), 500

    return jsonify({
        'success': True,
        'message': 'Course updated successfully',
        'course': course
    }), 200


@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Delete a specific course by its ID.
    Args:
        course_id: The ID of the course to delete.
    Returns:
        200 OK with deleted course data, or 404 if not found.
    """
    courses = load_courses()
    course_index = next((i for i, c in enumerate(courses) if c['id'] == course_id), None)
    if course_index is None:
        return jsonify({
            'success': False,
            'error': 'Course not found'
        }), 404

    deleted_course = courses.pop(course_index)
    if not save_courses(courses):
        return jsonify({
            'success': False,
            'error': 'Failed to delete course from data store'
        }), 500

    return jsonify({
        'success': True,
        'message': 'Course deleted successfully',
        'deleted_course': deleted_course
    }), 200


# ==============================================================================
# Bonus Challenge Endpoints: Statistics and Search
# ==============================================================================

@app.route('/api/courses/stats', methods=['GET'])
def get_course_stats():
    """
    Bonus Endpoint: Return summary statistics of courses in the platform.
    Counts total courses and tracks counts by status.
    """
    courses = load_courses()
    stats = {
        'total_courses': len(courses),
        'by_status': {
            'Not Started': sum(1 for c in courses if c.get('status') == 'Not Started'),
            'In Progress': sum(1 for c in courses if c.get('status') == 'In Progress'),
            'Completed': sum(1 for c in courses if c.get('status') == 'Completed')
        }
    }
    return jsonify({
        'success': True,
        'stats': stats
    }), 200


@app.route('/api/courses/search', methods=['GET'])
def search_courses():
    """
    Bonus Endpoint: Search courses by keyword in name or description.
    Query parameter:
        q: The search term (e.g., /api/courses/search?q=python)
    """
    query = request.args.get('q', '').strip().lower()
    courses = load_courses()
    if not query:
        return jsonify({
            'success': True,
            'query': '',
            'count': len(courses),
            'courses': courses
        }), 200

    matches = [
        c for c in courses
        if query in c.get('name', '').lower() or query in c.get('description', '').lower()
    ]
    return jsonify({
        'success': True,
        'query': query,
        'count': len(matches),
        'courses': matches
    }), 200


# ==============================================================================
# Error Handlers
# ==============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ==============================================================================
# Application Entry Point
# ==============================================================================

if __name__ == '__main__':
    print("CodeCraftHub API is starting...")
    print(f"Data will be stored in: {os.path.abspath(DATA_FILE)}")
    print("API will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
