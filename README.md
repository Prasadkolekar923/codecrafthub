# CodeCraftHub Learning Management System

> **Personalized Learning Platform for Developers**  
> *A lightweight, robust RESTful API built with Python and Flask to track courses and technical learning goals.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

---

## 📖 Project Overview

**CodeCraftHub** is a personalized learning management platform crafted specifically for developers. It enables engineers and learners to track courses they want to learn, monitor learning status, set target completion dates, and manage their educational roadmap.

The server-side component is designed as a clean, dependency-light REST API using **Python** and the **Flask** microframework. In accordance with project requirements, data is stored in a clean, human-readable **JSON file** (`courses.json`) without requiring heavy external database installations or complex authentication layers.

---

## ✨ Features

- **Full-Stack Learning Platform**:
  - **Interactive Single-Page Dashboard (`index.html`)**: Complete CRUD web interface built with vanilla HTML5, CSS3, and JavaScript (no heavy frontend frameworks).
  - **Theme & Design**: Professional purple (`#8B5CF6`), amber (`#F59E0B`), and red (`#EF4444`) color scheme with responsive card and table layout.
  - **Live Course Editing**: Edit modal with pre-filled inputs and real-time backend synchronization.
  - **Status Indicators**: Clean badges for `Not Started`, `In Progress`, and `Completed`.
  - **CORS Support**: Seamlessly connects whether launched via VS Code Live Server (port 5500) or directly through Flask.
- **Course Management API (CRUD)**:
  - **Create**: Add new courses with details, target dates, and statuses.
  - **Read**: Fetch all courses or retrieve specific courses by ID.
  - **Update**: Modify course details, descriptions, target dates, and statuses.
  - **Delete**: Remove completed or cancelled courses.
- **Auto-Persistence**: Seamlessly reads and writes to `courses.json`, auto-creating the file on first run.
- **Robust Error Handling**:
  - Validation for missing required fields (returns `400 Bad Request`).
  - Validation of status values (`Not Started`, `In Progress`, `Completed`).
  - Graceful handling of missing resources (returns `404 Not Found`).
  - JSON decode and I/O error protection.
- **Bonus Capabilities**:
  - **Statistics Endpoint**: Aggregates total courses and breakdown by completion status (`/api/courses/stats`).
  - **Search Endpoint**: Fast keyword search across course names and descriptions (`/api/courses/search?q=<term>`).
- **Comprehensive Testing Suite**: Includes automated unit tests (14 test cases in `test_app.py`) and executable curl / PowerShell scripts.

---

## 📁 Project Structure

```plaintext
codecrafthub/
├── app.py              # Main Flask application & REST API routes (with CORS & static serving)
├── index.html          # Single-page CRUD learning dashboard (HTML, CSS, JS)
├── courses.json        # Persistent JSON data store (auto-created on startup)
├── requirements.txt    # Python package dependencies (Flask, Werkzeug)
├── test_app.py         # Automated unit test suite (14 test cases)
├── test_endpoints.sh   # Automated curl test script for Bash / Linux / macOS
├── test_endpoints.ps1  # Automated test script for Windows PowerShell
├── .gitignore          # Git exclusion rules (cache, virtualenvs, etc.)
└── README.md           # Project documentation and API guide
```

---

## 🖥️ Running the Learning Dashboard

You can use the interactive dashboard in either of two ways:

### Option A: Directly Through Flask (Simplest)
1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```text
   http://localhost:5000/dashboard
   ```
   *(Or simply `http://localhost:5000` in any web browser)*

### Option B: Using VS Code / IDE Live Server
1. Ensure the Flask server is running on port 5000:
   ```bash
   python app.py
   ```
2. In VS Code or your IDE, right-click `index.html` and select **"Open with Live Server"**.
3. The dashboard will launch in your browser and automatically communicate with `http://localhost:5000/api/courses`.


---

## 🚀 Installation

Follow these step-by-step instructions to set up the project locally:

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd codecrafthub
```

### 2. (Optional but Recommended) Create a Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Application

Start the Flask development server:

```bash
python app.py
```

You should see output similar to:
```plaintext
CodeCraftHub API is starting...
Data will be stored in: C:\...\codecrafthub\courses.json
API will be available at: http://localhost:5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

---

## 📡 API Endpoints Documentation

### Summary Table

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API welcome message & route directory | `200 OK` |
| `GET` | `/api/courses` | Retrieve all courses | `200 OK` |
| `GET` | `/api/courses/<id>` | Retrieve a single course by ID | `200 OK` / `404 Not Found` |
| `POST` | `/api/courses` | Add a new course | `201 Created` / `400 Bad Request` |
| `PUT` | `/api/courses/<id>` | Update an existing course | `200 OK` / `404 Not Found` |
| `DELETE` | `/api/courses/<id>` | Delete a course | `200 OK` / `404 Not Found` |
| `GET` | `/api/courses/stats` | *(Bonus)* Get courses summary statistics | `200 OK` |
| `GET` | `/api/courses/search?q=<term>` | *(Bonus)* Search courses by keyword | `200 OK` |

---

### Detailed Endpoint Specifications

#### 1. Add a Course (POST `/api/courses`)
Creates a new course entry in the learning platform.

- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "name": "Python Basics",
    "description": "Learn Python fundamentals including variables, loops, and functions",
    "target_date": "2025-12-31",
    "status": "Not Started"
  }
  ```
  *Note: Allowed values for `status` are `"Not Started"`, `"In Progress"`, and `"Completed"`.*
- **Response (`201 Created`)**:
  ```json
  {
    "success": true,
    "message": "Course added successfully",
    "course": {
      "id": 1,
      "name": "Python Basics",
      "description": "Learn Python fundamentals including variables, loops, and functions",
      "target_date": "2025-12-31",
      "status": "Not Started",
      "created_at": "2025-11-18 20:45:00"
    }
  }
  ```

#### 2. Get All Courses (GET `/api/courses`)
Retrieves the list of all courses currently tracked.

- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "count": 1,
    "courses": [
      {
        "id": 1,
        "name": "Python Basics",
        "description": "Learn Python fundamentals including variables, loops, and functions",
        "target_date": "2025-12-31",
        "status": "Not Started",
        "created_at": "2025-11-18 20:45:00"
      }
    ]
  }
  ```

#### 3. Get Specific Course (GET `/api/courses/<id>`)
Retrieves details of a single course by its unique integer identifier.

- **Example**: `GET http://localhost:5000/api/courses/1`
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "course": {
      "id": 1,
      "name": "Python Basics",
      "description": "Learn Python fundamentals including variables, loops, and functions",
      "target_date": "2025-12-31",
      "status": "Not Started",
      "created_at": "2025-11-18 20:45:00"
    }
  }
  ```
- **Error Response (`404 Not Found`)**:
  ```json
  {
    "success": false,
    "error": "Course not found"
  }
  ```

#### 4. Update Course (PUT `/api/courses/<id>`)
Updates one or more fields of an existing course.

- **Headers**: `Content-Type: application/json`
- **Request Body (all fields optional)**:
  ```json
  {
    "status": "In Progress"
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Course updated successfully",
    "course": {
      "id": 1,
      "name": "Python Basics",
      "description": "Learn Python fundamentals including variables, loops, and functions",
      "target_date": "2025-12-31",
      "status": "In Progress",
      "created_at": "2025-11-18 20:45:00"
    }
  }
  ```

#### 5. Delete Course (DELETE `/api/courses/<id>`)
Removes a course from the platform.

- **Example**: `DELETE http://localhost:5000/api/courses/1`
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Course deleted successfully",
    "deleted_course": {
      "id": 1,
      "name": "Python Basics",
      "description": "Learn Python fundamentals including variables, loops, and functions",
      "target_date": "2025-12-31",
      "status": "In Progress",
      "created_at": "2025-11-18 20:45:00"
    }
  }
  ```

#### 6. Course Statistics (Bonus Endpoint) (GET `/api/courses/stats`)
Returns high-level statistics regarding the total courses and their breakdown by status.

- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "stats": {
      "total_courses": 3,
      "by_status": {
        "Not Started": 1,
        "In Progress": 1,
        "Completed": 1
      }
    }
  }
  ```

#### 7. Course Search (Bonus Endpoint) (GET `/api/courses/search?q=<term>`)
Filters courses whose title or description contains the search query.

- **Example**: `GET http://localhost:5000/api/courses/search?q=python`
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "query": "python",
    "count": 1,
    "courses": [...]
  }
  ```

---

## 🧪 Testing

### Automated Unit Testing
Run the Python unit test suite:

```bash
python -m unittest test_app.py -v
```

All 12 test scenarios run against an isolated test environment without touching your production `courses.json`.

### Testing with `curl` Commands

Ensure the server is running (`python app.py`), then run:

#### Test 1: Add Course (POST)
```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Basics",
    "description": "Learn Python fundamentals including variables, loops, and functions",
    "target_date": "2025-12-31",
    "status": "Not Started"
  }'
```

#### Test 2: Get All Courses (GET)
```bash
curl http://localhost:5000/api/courses
```

#### Test 3: Get Specific Course (GET)
```bash
curl http://localhost:5000/api/courses/1
```

#### Test 4: Update Course (PUT)
```bash
curl -X PUT http://localhost:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

#### Test 5: Delete Course (DELETE)
```bash
curl -X DELETE http://localhost:5000/api/courses/1
```

#### Test 6: Missing Required Field (Error Test)
```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete Course"}'
```
*Expected: 400 Bad Request with missing field message.*

#### Test 7: Invalid Status (Error Test)
```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Course",
    "description": "Test",
    "target_date": "2025-12-31",
    "status": "Invalid Status"
  }'
```
*Expected: 400 Bad Request with status validation message.*

#### Test 8: Course Not Found (Error Test)
```bash
curl http://localhost:5000/api/courses/999
```
*Expected: 404 Not Found.*

---

## 🛠️ Troubleshooting Common Issues

| Problem | Root Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'flask'` | Flask is not installed in current Python environment | Run `pip install -r requirements.txt` |
| `Address already in use` (Port 5000) | Another service (e.g. AirPlay on macOS or another Flask app) is using port 5000 | Either terminate the conflicting process or change the port in `app.py`: `app.run(port=5001)` |
| `Status must be one of: Not Started, In Progress, Completed` | Typo or lowercase in `status` field | Ensure exact match with `"Not Started"`, `"In Progress"`, or `"Completed"` |
| `JSONDecodeError` in `courses.json` | File was manually edited with invalid syntax | Delete or reset `courses.json` to `[]`. The app will auto-recreate it |

---

## 📜 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) for details.
