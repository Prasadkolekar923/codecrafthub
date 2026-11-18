"""
Automated Test Suite for CodeCraftHub API
Tests all CRUD operations, error scenarios, and bonus endpoints.
Uses a temporary JSON file so production courses.json is never modified during tests.
"""

import unittest
import json
import os
import app as application


class CodeCraftHubTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client and clean temporary test data file."""
        self.app = application.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Direct app to use a test-specific data file
        self.test_data_file = 'test_courses.json'
        application.DATA_FILE = self.test_data_file

        # Initialize with an empty test database
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

    def tearDown(self):
        """Clean up the temporary test data file after each test."""
        if os.path.exists(self.test_data_file):
            try:
                os.remove(self.test_data_file)
            except OSError:
                pass

    def test_root_endpoint(self):
        """Test GET / returns API welcome information."""
        response = self.client.get('/', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('endpoints', data)

    def test_dashboard_endpoint(self):
        """Test GET /dashboard returns the frontend HTML."""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CodeCraftHub: Your Learning Management Platform', response.data)

    def test_cors_headers(self):
        """Test that CORS headers are returned for frontend compatibility."""
        response = self.client.options('/api/courses')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')


    def test_get_empty_courses(self):
        """Test GET /api/courses when no courses exist."""
        response = self.client.get('/api/courses')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['courses'], [])

    def test_add_course_success(self):
        """Test 1: POST /api/courses successfully adds a new course."""
        payload = {
            "name": "Python Basics",
            "description": "Learn Python fundamentals including variables, loops, and functions",
            "target_date": "2025-12-31",
            "status": "Not Started"
        }
        response = self.client.post('/api/courses',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Course added successfully')
        self.assertEqual(data['course']['id'], 1)
        self.assertEqual(data['course']['name'], 'Python Basics')
        self.assertEqual(data['course']['status'], 'Not Started')
        self.assertIn('created_at', data['course'])

    def test_get_all_courses(self):
        """Test 2: GET /api/courses returns list of courses."""
        # Add a course first
        self.test_add_course_success()

        response = self.client.get('/api/courses')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['courses'][0]['name'], 'Python Basics')

    def test_get_specific_course(self):
        """Test 3: GET /api/courses/<id> retrieves existing course."""
        self.test_add_course_success()

        response = self.client.get('/api/courses/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['course']['id'], 1)

    def test_update_course(self):
        """Test 4: PUT /api/courses/<id> updates existing course."""
        self.test_add_course_success()

        update_payload = {"status": "In Progress"}
        response = self.client.put('/api/courses/1',
                                   data=json.dumps(update_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['course']['status'], 'In Progress')

    def test_delete_course(self):
        """Test 5: DELETE /api/courses/<id> deletes a course."""
        self.test_add_course_success()

        response = self.client.delete('/api/courses/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Course deleted successfully')

        # Verify deletion
        get_response = self.client.get('/api/courses/1')
        self.assertEqual(get_response.status_code, 404)

    def test_missing_required_fields(self):
        """Test 6: POST /api/courses fails when required field is missing."""
        payload = {"name": "Incomplete Course"}
        response = self.client.post('/api/courses',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('Missing required field', data['error'])

    def test_invalid_status_value(self):
        """Test 7: POST /api/courses fails with invalid status value."""
        payload = {
            "name": "Test Course",
            "description": "Test",
            "target_date": "2025-12-31",
            "status": "Invalid Status"
        }
        response = self.client.post('/api/courses',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('Status must be one of', data['error'])

    def test_course_not_found(self):
        """Test 8: GET /api/courses/999 returns 404 when course does not exist."""
        response = self.client.get('/api/courses/999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Course not found')

    def test_bonus_stats_endpoint(self):
        """Test bonus GET /api/courses/stats endpoint."""
        # Add 2 courses
        c1 = {"name": "Python", "description": "Desc", "target_date": "2025-12-31", "status": "Not Started"}
        c2 = {"name": "Flask", "description": "Desc", "target_date": "2025-12-31", "status": "Completed"}
        self.client.post('/api/courses', data=json.dumps(c1), content_type='application/json')
        self.client.post('/api/courses', data=json.dumps(c2), content_type='application/json')

        response = self.client.get('/api/courses/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['stats']['total_courses'], 2)
        self.assertEqual(data['stats']['by_status']['Not Started'], 1)
        self.assertEqual(data['stats']['by_status']['Completed'], 1)

    def test_bonus_search_endpoint(self):
        """Test bonus GET /api/courses/search endpoint."""
        c1 = {"name": "Python Basics", "description": "Intro to Python", "target_date": "2025-12-31", "status": "Not Started"}
        c2 = {"name": "JavaScript Advanced", "description": "Async JS", "target_date": "2025-12-31", "status": "In Progress"}
        self.client.post('/api/courses', data=json.dumps(c1), content_type='application/json')
        self.client.post('/api/courses', data=json.dumps(c2), content_type='application/json')

        response = self.client.get('/api/courses/search?q=python')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['courses'][0]['name'], 'Python Basics')


if __name__ == '__main__':
    unittest.main()
