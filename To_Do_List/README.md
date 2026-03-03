# To-Do List API

A FastAPI-based RESTful API for managing to-do tasks with user authentication and authorization. This project includes a full-stack solution with a Python backend and a JavaScript frontend.

## Features

- **User Authentication**
  - User registration with email and password
  - Login with JWT token-based authentication
  - Secure password hashing with bcrypt
  - Token expiration (30 minutes)

- **Task Management**
  - Create, read, update, and delete tasks
  - Tasks are user-specific (only owners can access their tasks)
  - Task properties: title, description, completion status

- **Frontend Interface**
  - HTML-based user interface
  - JavaScript client for API interaction
  - Responsive design with integrated templates

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** SQLAlchemy ORM with configurable database
- **Authentication:** JWT (JSON Web Tokens) with passlib
- **Password Hashing:** bcrypt
- **Frontend:** HTML/JavaScript

## Project Structure

```
To_Do_List/
├── auth.py              # Authentication logic (JWT, password hashing)
├── database.py          # Database configuration and session management
├── deps.py              # Dependency injection (get_current_user)
├── main.py              # FastAPI application and route handlers
├── models.py            # SQLAlchemy ORM models (User, Task)
├── schemas.py           # Pydantic schemas for request/response validation
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Frontend HTML template
└── scripts/
    └── index.js         # Frontend JavaScript client
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip or virtualenv

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd To_Do_List
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=sqlite:///./test.db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ```

## Running the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- **POST** `/register` - Register a new user
  - Request body: `{"email": "user@example.com", "password": "password123"}`

- **POST** `/login` - Login and get JWT token
  - Request body: `{"username": "user@example.com", "password": "password123"}`
  - Response: `{"access_token": "token", "token_type": "bearer"}`

### Tasks

- **POST** `/tasks` - Create a new task (requires authentication)
  - Request body: `{"title": "Task title", "description": "Task description"}`

- **GET** `/tasks` - Get all tasks for the current user (requires authentication)

- **PUT** `/tasks/{task_id}` - Update a task (requires authentication)
  - Request body: `{"title": "Updated title", "description": "Updated description"}`

- **DELETE** `/tasks/{task_id}` - Delete a task (requires authentication)

### Frontend

- **GET** `/` - Serve the main HTML interface

## Models

### User
- `id` (Integer, Primary Key)
- `email` (String, Unique)
- `hashed_password` (String)
- `tasks` (Relationship to Task)

### Task
- `id` (Integer, Primary Key)
- `title` (String)
- `description` (String)
- `is_completed` (Boolean, default: False)
- `owner_id` (Foreign Key to User)
- `owner` (Relationship to User)

## Authentication Flow

1. User registers with email and password
2. Password is hashed using bcrypt
3. User logs in with email and password
4. Server validates credentials and returns JWT token
5. Client includes token in Authorization header for subsequent requests: `Authorization: Bearer <token>`
6. Token expires after 30 minutes

## Environment Variables

Create a `.env` file with the following variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./test.db` or `postgresql://user:password@localhost/dbname` |
| `SECRET_KEY` | Secret key for JWT signing | Random secure string |
| `ALGORITHM` | JWT algorithm | `HS256` |

## Development

### Running Tests
```bash
# Add test dependencies and run tests as needed
pytest
```

### Code Style
Feel free to format code according to your preferences using tools like:
- `black` - Code formatter
- `flake8` - Linter
- `pylint` - Code analysis

## Future Enhancements

- [ ] Task categories/tags
- [ ] Task priority levels
- [ ] Due dates and reminders
- [ ] Task sharing between users
- [ ] Email verification on registration
- [ ] Password reset functionality
- [ ] Improved frontend UI with frameworks (React, Vue)
- [ ] WebSocket support for real-time updates
- [ ] API documentation with Swagger UI
- [ ] Unit and integration tests

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on the repository or contact the development team.
