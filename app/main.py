
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text, asc, desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal, get_db
from app import models
from app.models import Employee, User, Department

from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    UserCreate,
    UserResponse,
    UserLogin,
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate
)

from pwdlib import PasswordHash
from app.auth import create_access_token
from app.auth import get_current_user,get_admin_user

password_hash = PasswordHash.recommended()


app=FastAPI(
    title="Employee Management API",
    description="REST API for managing employees",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

@app.post("/departments", response_model=DepartmentResponse)
def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    existing_department = db.query(Department).filter(
        Department.name.ilike(department_data.name)
    ).first()

    if existing_department:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    new_department = Department(
        name=department_data.name,
        description=department_data.description
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department
@app.get("/departments", response_model=list[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    departments = db.query(Department).order_by(
        Department.id.asc()
    ).all()

    return departments



@app.get("/departments/statistics")
def department_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(
        Department.id,
        Department.name,
        func.count(Employee.id).label("total_employees"),
        func.count(Employee.id).filter(
            Employee.is_active == True
        ).label("active_employees"),
        func.count(Employee.id).filter(
            Employee.is_active == False
        ).label("inactive_employees")
    ).outerjoin(
        Employee,
        Department.id == Employee.department_id
    ).group_by(
        Department.id,
        Department.name
    ).order_by(
        Department.id.asc()
    ).all()

    return [
        {
            "department_id": row.id,
            "department_name": row.name,
            "total_employees": row.total_employees,
            "active_employees": row.active_employees,
            "inactive_employees": row.inactive_employees
        }
        for row in results
    ]






@app.get("/departments/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    return department


@app.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    existing_department = db.query(Department).filter(
        Department.name.ilike(department_data.name),
        Department.id != department_id
    ).first()

    if existing_department:
        raise HTTPException(status_code=400, detail="Department name already exists")

    department.name = department_data.name
    department.description = department_data.description

    db.commit()
    db.refresh(department)

    return department






@app.delete("/departments/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    if department.employees:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete department because employees are assigned to it"
        )

    db.delete(department)
    db.commit()

    return {"message": "Department deleted successfully"}

@app.get("/")
def home():
    return{
        "message": "Welcome to Employee Management API",
        "status": "Running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }

@app.get("/db-check")
def database_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "message": "PostgreSQL connected successfully!"
    }







@app.post("/employees")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    try:
        department = db.query(Department).filter(
            Department.id == employee.department_id
        ).first()

        if department is None:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        new_employee = Employee(
            name=employee.name,
            email=employee.email,
            department=department.name,
            department_id=employee.department_id,
            salary=employee.salary,
            is_active=employee.is_active
        )

        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return {
            "message": "Employee created successfully",
            "employee": {
                "id": new_employee.id,
                "name": new_employee.name,
                "email": new_employee.email,
                "department_id": new_employee.department_id,
                "department": department.name,
                "salary": new_employee.salary,
                "is_active": new_employee.is_active
            }
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employee email already exists"
        )







@app.get("/employees")
def get_employees(
    search: str = None,
    department: str = None,
    department_id: int = None,
    is_active: bool = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("id", pattern="^(id|name|salary)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Employee)

    if search:
        query = query.filter(
            Employee.name.ilike(f"%{search}%")
        )

    if department:
        query = query.join(Department).filter(
            Department.name.ilike(f"%{department}%")
        )

    if department_id is not None:
        query = query.filter(
            Employee.department_id == department_id
        )

    if is_active is not None:
        query = query.filter(
            Employee.is_active == is_active
        )

    if sort_by == "name":
        column = Employee.name
    elif sort_by == "salary":
        column = Employee.salary
    else:
        column = Employee.id

    if order == "desc":
        query = query.order_by(desc(column))
    else:
        query = query.order_by(asc(column))

    employees = query.offset(skip).limit(limit).all()

    return [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "department_id": emp.department_id,
            "department": emp.department_info.name,
            "salary": emp.salary,
            "is_active": emp.is_active
        }
        for emp in employees
    ]








@app.get("/employees/count")
def employee_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Employee).count()

    return {
        "total_employees": total
    }






@app.get("/employees/statistics")
def employee_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Employee).count()

    active = db.query(Employee).filter(
        Employee.is_active == True
    ).count()

    inactive = db.query(Employee).filter(
        Employee.is_active == False
    ).count()

    return {
        "total_employees": total,
        "active_employees": active,
        "inactive_employees": inactive
    }






@app.get("/employees/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "department_id": employee.department_id,
        "department": employee.department_info.name,
        "salary": employee.salary,
        "is_active": employee.is_active
    }











@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    try:
        employee = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        department = db.query(Department).filter(
            Department.id == employee_data.department_id
        ).first()

        if department is None:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        employee.name = employee_data.name
        employee.email = employee_data.email
        employee.department = department.name
        employee.department_id = employee_data.department_id
        employee.salary = employee_data.salary
        employee.is_active = employee_data.is_active

        db.commit()
        db.refresh(employee)

        return {
            "message": "Employee updated successfully",
            "employee": {
                "id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "department_id": employee.department_id,
                "department": department.name,
                "salary": employee.salary,
                "is_active": employee.is_active
            }
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employee email already exists"
        )










@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    try:
        employee = db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        db.delete(employee)
        db.commit()

        return {
            "message": "Employee deleted successfully"
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting employee"
        )








@app.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        # Check existing username
        existing_user = db.query(User).filter(
            User.username == user_data.username
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        # Check existing email
        existing_email = db.query(User).filter(
            User.email == user_data.email
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = password_hash.hash(
            user_data.password
        )

        # Create new user
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )








@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    is_password_correct = password_hash.verify(
        form_data.password,
        user.hashed_password
    )

    if not is_password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }







@app.get("/users/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }