#!/usr/bin/env bash
# ==============================================================================
# CodeCraftHub API Test Script (curl)
# Tests all endpoints and error cases sequentially against http://localhost:5000
# ==============================================================================

BASE_URL="http://localhost:5000"

echo "========================================="
echo "Testing CodeCraftHub Learning Platform API"
echo "========================================="

echo -e "\n[Test 1] Add a New Course (POST /api/courses)"
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Basics",
    "description": "Learn Python fundamentals including variables, loops, and functions",
    "target_date": "2025-12-31",
    "status": "Not Started"
  }'

echo -e "\n\n[Test 2] Get All Courses (GET /api/courses)"
curl -i "$BASE_URL/api/courses"

echo -e "\n\n[Test 3] Get Specific Course (GET /api/courses/1)"
curl -i "$BASE_URL/api/courses/1"

echo -e "\n\n[Test 4] Update Course (PUT /api/courses/1)"
curl -i -X PUT "$BASE_URL/api/courses/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'

echo -e "\n\n[Test 5] Error Case: Missing Required Fields (POST /api/courses)"
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete Course"}'

echo -e "\n\n[Test 6] Error Case: Invalid Status Value (POST /api/courses)"
curl -i -X POST "$BASE_URL/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Course",
    "description": "Test",
    "target_date": "2025-12-31",
    "status": "Invalid Status"
  }'

echo -e "\n\n[Test 7] Error Case: Course Not Found (GET /api/courses/999)"
curl -i "$BASE_URL/api/courses/999"

echo -e "\n\n[Test 8] Bonus Challenge: Course Statistics (GET /api/courses/stats)"
curl -i "$BASE_URL/api/courses/stats"

echo -e "\n\n[Test 9] Bonus Challenge: Search Courses (GET /api/courses/search?q=python)"
curl -i "$BASE_URL/api/courses/search?q=python"

echo -e "\n\n[Test 10] Delete Course (DELETE /api/courses/1)"
curl -i -X DELETE "$BASE_URL/api/courses/1"

echo -e "\n\n[Test 11] Verify Deletion (GET /api/courses/1)"
curl -i "$BASE_URL/api/courses/1"

echo -e "\n\nAll tests completed!"
