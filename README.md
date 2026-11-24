# Employee Management API

A RESTful Employee Management API built using **FastAPI, Python, SQLAlchemy, and PostgreSQL**. The application provides employee and department management, JWT-based authentication, role-based authorization, and automated API testing.

## Features

- Employee CRUD operations (Create, Read, Update, Delete)
- Department CRUD operations
- Employee and department statistics
- User registration and login
- JWT-based authentication
- Password hashing and verification using pwdlib
- Role-based access control (Admin and User)
- Active/inactive user account management
- Database health-check endpoints
- Automated testing using Pytest

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (PyJWT)
- **Password Security:** pwdlib
- **Validation:** Pydantic
- **Server:** Uvicorn
- **Testing:** Pytest

## Project Structure

```text
employee-management-api/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── conftest.py
│   └── test_main.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── .env.example
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/employee-management-api.git
cd employee-management-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secure_random_secret
```

Replace the placeholder values with your own PostgreSQL connection string and a securely generated JWT secret.

Never commit your `.env` file to GitHub.

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

## API Documentation

FastAPI automatically generates interactive API documentation.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate user |
| GET | `/users/me` | Get current user profile |

### Employees

| Method | Endpoint | Description |
|---|---|---|
| POST | `/employees` | Create employee |
| GET | `/employees` | List employees |
| GET | `/employees/count` | Get employee count |
| GET | `/employees/statistics` | Employee statistics |
| GET | `/employees/{employee_id}` | Get employee details |
| PUT | `/employees/{employee_id}` | Update employee |
| DELETE | `/employees/{employee_id}` | Delete employee |

### Departments

| Method | Endpoint | Description |
|---|---|---|
| POST | `/departments` | Create department |
| GET | `/departments` | List departments |
| GET | `/departments/statistics` | Department statistics |
| GET | `/departments/{department_id}` | Get department details |
| PUT | `/departments/{department_id}` | Update department |
| DELETE | `/departments/{department_id}` | Delete department |

### System

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home endpoint |
| GET | `/health` | Health check |
| GET | `/db-check` | Database connectivity check |

## Authentication and Security

- JWT tokens are used for authenticated API requests.
- Passwords are hashed using pwdlib.
- Protected endpoints require valid authentication.
- Admin-only operations use role-based authorization.
- Inactive accounts cannot access protected resources.
- JWT secrets and database credentials are configured through environment variables.

## Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

The project currently has **38 passing automated tests**.

## Future Improvements

- Add database migrations using Alembic.
- Add Docker support.
- Implement pagination and advanced filtering.
- Add API deployment and CI/CD integration.

## Author

**Aryan Sutradhar**

GitHub: [aryansutradhar](https://github.com/aryansutradhar)
