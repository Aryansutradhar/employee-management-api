# Employee Management API

A RESTful Employee Management API built using **Python, FastAPI, SQLAlchemy, and PostgreSQL**. This project provides employee and department management, JWT-based authentication, role-based access control, and automated API testing.

The application follows a structured backend architecture with secure authentication, database integration, request validation, and protected API endpoints.

## Features

- **Employee Management:** Create, retrieve, update, and delete employee records.
- **Department Management:** Create, retrieve, update, and delete departments.
- **Employee Statistics:** Retrieve employee counts and statistics.
- **Department Statistics:** Retrieve department-related statistics.
- **User Registration:** Register new users securely.
- **JWT Authentication:** Secure login and token-based authentication.
- **Password Security:** Password hashing and verification using `pwdlib`.
- **Role-Based Access Control (RBAC):** Separate permissions for Admin and User roles.
- **Account Management:** Support for active and inactive user accounts.
- **Database Health Checks:** Monitor API and database connectivity.
- **Automated Testing:** Test API functionality and authentication using Pytest.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Pydantic | Data validation and serialization |
| PyJWT | JWT authentication |
| pwdlib | Password hashing and verification |
| Uvicorn | ASGI server |
| Pytest | Automated testing |

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
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Aryansutradhar/employee-management-api.git
```

Navigate to the project directory:

```bash
cd employee-management-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory.

Add the following environment variables:

```env
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secure_random_secret
```

Replace the placeholder values with your actual PostgreSQL database connection URL and a securely generated JWT secret key.

**Important:** Never upload your actual `.env` file or expose database credentials and secret keys on GitHub.

### 6. Run the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The application will run locally at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

Once the application is running, access:

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

Swagger UI allows you to interact with and test the API endpoints directly from your browser.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate a user |
| GET | `/users/me` | Retrieve the current user's profile |

### Employee Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/employees` | Create a new employee |
| GET | `/employees` | Retrieve all employees |
| GET | `/employees/count` | Get total employee count |
| GET | `/employees/statistics` | Retrieve employee statistics |
| GET | `/employees/{employee_id}` | Retrieve employee details |
| PUT | `/employees/{employee_id}` | Update employee details |
| DELETE | `/employees/{employee_id}` | Delete an employee |

### Department Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/departments` | Create a new department |
| GET | `/departments` | Retrieve all departments |
| GET | `/departments/statistics` | Retrieve department statistics |
| GET | `/departments/{department_id}` | Retrieve department details |
| PUT | `/departments/{department_id}` | Update department details |
| DELETE | `/departments/{department_id}` | Delete a department |

### System Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home endpoint |
| GET | `/health` | Application health check |
| GET | `/db-check` | Database connectivity check |

## Authentication and Security

The application implements authentication and authorization to protect sensitive API operations.

- **JWT Authentication:** Uses JSON Web Tokens to authenticate API requests.
- **Password Hashing:** Passwords are securely hashed using `pwdlib`.
- **Protected Endpoints:** Restricted endpoints require valid authentication.
- **Role-Based Authorization:** Admin-only operations are protected using role-based access control.
- **Account Status Management:** Inactive accounts cannot access protected resources.
- **Environment Configuration:** Database credentials and JWT secrets are managed through environment variables.

## Automated Testing

The project includes automated API tests using **Pytest**.

The test suite covers application functionality, employee and department operations, authentication, authorization, and access restrictions.

Run the complete test suite using:

```bash
python -m pytest -v
```

### Test Results

**38 automated tests passing successfully.**

The tests help verify that the API behaves as expected and that authentication and authorization rules are enforced.

## Future Improvements

Potential improvements for future development include:

- Database migrations using Alembic.
- Docker containerization.
- Pagination and advanced filtering.
- API deployment to a cloud platform.
- CI/CD integration using GitHub Actions.
- Improved logging and monitoring.

## Author

**Aryan Sutradhar**

Computer Science and Engineering

GitHub: [@Aryansutradhar](https://github.com/Aryansutradhar)

## Project Repository

[Employee Management API – GitHub](https://github.com/Aryansutradhar/employee-management-api)

---

**Built with Python, FastAPI, PostgreSQL, and SQLAlchemy.**
