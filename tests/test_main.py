
from app.models import User, Employee, Department
from app.auth import create_access_token
from app import main
from sqlalchemy import text


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to Employee Management API",
        "status": "Running"
    }



def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "Healthy"
    }




def test_database_check_endpoint(client):
    response = client.get("/db-check")

    assert response.status_code == 200

    assert response.json() == {
        "message": "PostgreSQL connected successfully!"
    }


def test_employee_count_endpoint(client):

    db = main.SessionLocal()

    test_user = User(
        username="pytest_user",
        email="pytest@example.com",
        hashed_password="test_password"
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    db.close()

    response = client.get(
        "/employees/count",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert "total_employees" in response.json()






def test_employee_statistics_endpoint(client):

    db = main.SessionLocal()

    test_user = User(
        username="stats_user",
        email="stats@example.com",
        hashed_password="test_password"
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    db.close()

    response = client.get(
        "/employees/statistics",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_employees" in data
    assert "active_employees" in data
    assert "inactive_employees" in data





def test_get_employees_endpoint(client):

    db = main.SessionLocal()

    test_user = User(
        username="employee_list_user",
        email="list@example.com",
        hashed_password="test_password"
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    db.close()

    response = client.get(
        "/employees",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)





def test_get_employee_not_found(client):

    db = main.SessionLocal()

    test_user = User(
        username="notfound_user",
        email="notfound@example.com",
        hashed_password="test_password"
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    db.close()

    response = client.get(
        "/employees/99999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    assert response.json()["detail"] == "Employee not found"






def test_employee_endpoint_without_token(client):

    response = client.get("/employees")

    assert response.status_code == 401

    assert response.json()["detail"] == "Not authenticated"





def test_user_registration(client):

    response = client.post(
        "/register",
        json={
            "username": "new_test_user",
            "email": "newtest@example.com",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "new_test_user"
    assert data["email"] == "newtest@example.com"
    assert "hashed_password" not in data



def test_duplicate_username_registration(client):

    user_data = {
        "username": "duplicate_user",
        "email": "duplicate1@example.com",
        "password": "Test@12345"
    }

    first_response = client.post(
        "/register",
        json=user_data
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/register",
        json={
            "username": "duplicate_user",
            "email": "duplicate2@example.com",
            "password": "Test@12345"
        }
    )

    assert second_response.status_code == 400

    assert second_response.json()["detail"] == "Username already exists"





def test_user_login(client):

    client.post(
        "/register",
        json={
            "username": "login_test_user",
            "email": "login@example.com",
            "password": "Test@12345"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "login_test_user",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["token_type"] == "bearer"
    assert "access_token" in data




def test_login_with_wrong_password(client):

    client.post(
        "/register",
        json={
            "username": "wrongpass_user",
            "email": "wrongpass@example.com",
            "password": "Test@12345"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "wrongpass_user",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid username or password"






def test_get_departments(client):

    db = main.SessionLocal()

    test_user = User(
        username="department_user",
        email="department@example.com",
        hashed_password="test_password"
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    db.close()

    response = client.get(
        "/departments",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)





def test_department_statistics(client):

    db = main.SessionLocal()

    test_user = User(
        username="dept_stats_user",
        email="deptstats@example.com",
        hashed_password="test_password"
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    db.close()

    response = client.get(
        "/departments/statistics",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)




def test_department_access_without_token(client):

    response = client.get("/departments")

    assert response.status_code == 401

    assert response.json()["detail"] == "Not authenticated"





def test_inactive_user_cannot_access_employees(client):

    db = main.SessionLocal()

    test_user = User(
        username="inactive_user",
        email="inactive@example.com",
        hashed_password="test_password",
        is_active=False
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    db.close()

    response = client.get(
        "/employees",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "User account is inactive"



def test_inactive_user_cannot_access_departments(client):

    db = main.SessionLocal()

    test_user = User(
        username="inactive_dept_user",
        email="inactivedept@example.com",
        hashed_password="test_password",
        is_active=False
    )

    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    db.close()

    response = client.get(
        "/departments",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "User account is inactive"






def test_create_employee_without_token(client):

    response = client.post(
        "/employees",
        json={
            "name": "Unauthorized Employee",
            "email": "unauthorized@example.com",
            "department_id": 1
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"






def test_create_department_without_token(client):

    response = client.post(
        "/departments",
        json={
            "name": "Unauthorized Department",
            "description": "Testing unauthorized access"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"





def test_update_employee_without_token(client):

    response = client.put(
        "/employees/1",
        json={
            "name": "Updated Unauthorized Employee",
            "email": "updated@example.com",
            "department_id": 1
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"





def test_delete_employee_without_token(client):

    response = client.delete("/employees/1")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"



def test_delete_department_without_token(client):

    response = client.delete("/departments/1")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"




def test_login_with_unregistered_username(client):

    response = client.post(
        "/login",
        data={
            "username": "unknown_user",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == "Invalid username or password"



def test_duplicate_email_registration(client):

    first_response = client.post(
        "/register",
        json={
            "username": "email_user1",
            "email": "sameemail@example.com",
            "password": "Test@12345"
        }
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/register",
        json={
            "username": "email_user2",
            "email": "sameemail@example.com",
            "password": "Test@12345"
        }
    )

    assert second_response.status_code == 400

    assert second_response.json()["detail"] == "Email already registered"





def test_inactive_user_cannot_login(client):

    db = main.SessionLocal()

    test_user = User(
        username="inactive_login",
        email="inactivelogin@example.com",
        hashed_password=main.password_hash.hash("test_password"),
        is_active=False
    )

    db.add(test_user)
    db.commit()
    db.close()

    response = client.post(
        "/login",
        data={
            "username": "inactive_login",
            "password": "test_password"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Account is inactive"






def test_login_token_accesses_employees(client):
    client.post("/register", json={
        "username": "token_access_user",
        "email": "tokenaccess@example.com",
        "password": "Test@12345"
    })

    login = client.post("/login", data={
        "username": "token_access_user",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        "/employees",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)





def test_employee_access_with_invalid_token(client):
    response = client.get(
        "/employees",
        headers={
            "Authorization": "Bearer invalid_fake_token"
        }
    )

    assert response.status_code == 401





def test_employee_access_with_empty_bearer_token(client):
    response = client.get(
        "/employees",
        headers={
            "Authorization": "Bearer "
        }
    )

    assert response.status_code == 401





def test_create_employee_with_valid_token(client):
    db = main.SessionLocal()

    test_user = User(
        username="employee_creator",
        email="creator@example.com",
        hashed_password=main.password_hash.hash("Test@12345"),
        role="admin",
        is_active=True
    )

    department = Department(
        name="JWT Test Department",
        description="Department for JWT employee testing"
    )

    db.add(test_user)
    db.add(department)
    db.commit()

    department_id = department.id

    db.close()

    login = client.post("/login", data={
        "username": "employee_creator",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        "/employees",
        json={
        "name": "JWT Test Employee",
        "email": "jwtemployee@example.com",
        "department_id": department_id,
        "salary": 35000
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200
    assert response.json()["employee"]["name"] == "JWT Test Employee"






def test_normal_user_cannot_create_employee(client):
    client.post("/register", json={
        "username": "normal_creator",
        "email": "normalcreator@example.com",
        "password": "Test@12345"
    })

    login = client.post("/login", data={
        "username": "normal_creator",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        "/employees",
        json={
            "name": "Unauthorized Employee",
            "email": "unauthorized@example.com",
            "department_id": 1,
            "salary": 30000
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"






def test_admin_can_create_department(client):
    db = main.SessionLocal()

    test_user = User(
        username="department_admin",
        email="departmentadmin@example.com",
        hashed_password=main.password_hash.hash("Test@12345"),
        role="admin",
        is_active=True
    )

    db.add(test_user)
    db.commit()
    db.close()

    login = client.post("/login", data={
        "username": "department_admin",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        "/departments",
        json={
            "name": "Testing Department",
            "description": "Created through admin authentication"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Testing Department"







def test_normal_user_cannot_create_department(client):
    client.post("/register", json={
        "username": "normal_dept_user",
        "email": "normaldept@example.com",
        "password": "Test@12345"
    })

    login = client.post("/login", data={
        "username": "normal_dept_user",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.post(
        "/departments",
        json={
            "name": "Unauthorized Department",
            "description": "Should not be created"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"





def test_admin_can_update_employee(client):
    db = main.SessionLocal()

    # 1. Create admin user
    test_user = db.query(User).filter(
        User.username == "update_admin"
    ).first()

    if not test_user:
        test_user = User(
            username="update_admin",
            email="updateadmin@example.com",
            hashed_password=main.password_hash.hash("Test@12345"),
            role="admin",
            is_active=True
        )
        db.add(test_user)
    else:
        test_user.hashed_password = main.password_hash.hash("Test@12345")
        test_user.role = "admin"
        test_user.is_active = True

    db.commit()

    # 2. Create department
    test_department = db.query(Department).filter(
        Department.name == "JWT Test Department"
    ).first()

    if not test_department:
        test_department = Department(
            name="JWT Test Department",
            description="Department for JWT testing"
        )
        db.add(test_department)
        db.commit()
        db.refresh(test_department)

    # 3. Create employee
    test_employee = Employee(
        name="JWT Test Employee",
        email="jwtemployee@example.com",
        department="JWT Test Department",
        department_id=test_department.id,
        salary=40000,
        is_active=True
    )

    db.add(test_employee)
    db.commit()
    db.refresh(test_employee)

    employee_id = test_employee.id
    department_id = test_department.id

    db.close()

    # 4. Login as admin
    login = client.post("/login", data={
        "username": "update_admin",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    # 5. Update employee
    response = client.put(
        f"/employees/{employee_id}",
        json={
            "name": "Updated JWT Employee",
            "email": "updatedjwt@example.com",
            "department": "JWT Test Department",
            "department_id": department_id,
            "salary": 45000,
            "is_active": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200





def test_normal_user_cannot_update_employee(client):
    db = main.SessionLocal()

    # Create normal user
    test_user = User(
        username="normal_update_user",
        email="normalupdate@example.com",
        hashed_password=main.password_hash.hash("Test@12345"),
        role="user",
        is_active=True
    )

    # Create department
    department = Department(
        name="Normal Update Department",
        description="Testing normal user permissions"
    )

    db.add(test_user)
    db.add(department)
    db.commit()
    db.refresh(department)

    # Create employee
    test_employee = Employee(
        name="Normal Update Employee",
        email="normalupdateemployee@example.com",
        department="Normal Update Department",
        department_id=department.id,
        salary=30000,
        is_active=True
    )

    db.add(test_employee)
    db.commit()
    db.refresh(test_employee)
    department_id = department.id

    employee_id = test_employee.id

    db.close()

    # Login as normal user
    login = client.post("/login", data={
        "username": "normal_update_user",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    # Attempt to update employee
    response = client.put(
        f"/employees/{employee_id}",
        json={
            "name": "Unauthorized Update",
            "email": "unauthorizedupdate@example.com",
            "department_id": department_id,
            "salary": 50000,
            "is_active": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"




def test_normal_user_cannot_delete_employee(client):
    db = main.SessionLocal()

    # Create normal user
    test_user = db.query(User).filter(
        User.username == "normal_delete_user"
    ).first()

    if not test_user:
        test_user = User(
            username="normal_delete_user",
            email="normaldelete@example.com",
            hashed_password=main.password_hash.hash("Test@12345"),
            role="user",
            is_active=True
        )
        db.add(test_user)
    else:
        test_user.hashed_password = main.password_hash.hash("Test@12345")
        test_user.role = "user"
        test_user.is_active = True

    # Create department
    department = db.query(Department).filter(
        Department.name == "Delete Test Department"
    ).first()

    if not department:
        department = Department(
            name="Delete Test Department",
            description="Testing delete permissions"
        )
        db.add(department)
        db.commit()
        db.refresh(department)

    department_id = department.id

    # Create employee
    test_employee = db.query(Employee).filter(
        Employee.email == "normaldeleteemployee@example.com"
    ).first()

    if not test_employee:
        test_employee = Employee(
            name="Delete Test Employee",
            email="normaldeleteemployee@example.com",
            department="Delete Test Department",
            department_id=department_id,
            salary=30000,
            is_active=True
        )
        db.add(test_employee)
        db.commit()
        db.refresh(test_employee)

    employee_id = test_employee.id

    db.commit()
    db.close()

    # Login as normal user
    login = client.post("/login", data={
        "username": "normal_delete_user",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    # Attempt to delete employee
    response = client.delete(
        f"/employees/{employee_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"




def test_admin_can_delete_employee(client):
    db = main.SessionLocal()

    # Create admin user
    test_user = db.query(User).filter(
        User.username == "delete_admin"
    ).first()

    if not test_user:
        test_user = User(
            username="delete_admin",
            email="deleteadmin@example.com",
            hashed_password=main.password_hash.hash("Test@12345"),
            role="admin",
            is_active=True
        )
        db.add(test_user)
    else:
        test_user.hashed_password = main.password_hash.hash("Test@12345")
        test_user.role = "admin"
        test_user.is_active = True

    # Create department
    department = db.query(Department).filter(
        Department.name == "Admin Delete Department"
    ).first()

    if not department:
        department = Department(
            name="Admin Delete Department",
            description="Testing admin delete permissions"
        )
        db.add(department)
        db.commit()
        db.refresh(department)

    department_id = department.id

    # Create employee
    test_employee = Employee(
        name="Admin Delete Employee",
        email="admindeleteemployee@example.com",
        department="Admin Delete Department",
        department_id=department_id,
        salary=35000,
        is_active=True
    )

    db.add(test_employee)
    db.commit()
    db.refresh(test_employee)

    employee_id = test_employee.id
    db.close()

    # Login as admin
    login = client.post("/login", data={
        "username": "delete_admin",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    # Delete employee
    response = client.delete(
        f"/employees/{employee_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200

    # Verify employee is deleted
    db = main.SessionLocal()

    deleted_employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    assert deleted_employee is None

    db.close()







def test_admin_can_delete_department(client):
    db = main.SessionLocal()

    # Create admin user
    test_user = db.query(User).filter(
        User.username == "delete_dept_admin"
    ).first()

    if not test_user:
        test_user = User(
            username="delete_dept_admin",
            email="deletedeptadmin@example.com",
            hashed_password=main.password_hash.hash("Test@12345"),
            role="admin",
            is_active=True
        )
        db.add(test_user)
    else:
        test_user.hashed_password = main.password_hash.hash("Test@12345")
        test_user.role = "admin"
        test_user.is_active = True

    # Create department
    department = Department(
        name="Admin Delete Test Department",
        description="Testing department deletion"
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    department_id = department.id
    db.close()

    # Login as admin
    login = client.post("/login", data={
        "username": "delete_dept_admin",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    # Delete department
    response = client.delete(
        f"/departments/{department_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200

    # Verify department is deleted
    db = main.SessionLocal()

    deleted_department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    assert deleted_department is None

    db.close()





def test_normal_user_cannot_delete_department(client):
    db = main.SessionLocal()

    # Create normal user
    test_user = db.query(User).filter(
        User.username == "normal_delete_dept"
    ).first()

    if not test_user:
        test_user = User(
            username="normal_delete_dept",
            email="normaldeletedept@example.com",
            hashed_password=main.password_hash.hash("Test@12345"),
            role="user",
            is_active=True
        )
        db.add(test_user)
    else:
        test_user.hashed_password = main.password_hash.hash("Test@12345")
        test_user.role = "user"
        test_user.is_active = True

    # Create department
    department = Department(
        name="Normal Delete Test Department",
        description="Testing normal user department deletion"
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    department_id = department.id
    db.close()

    # Login as normal user
    login = client.post("/login", data={
        "username": "normal_delete_dept",
        "password": "Test@12345"
    })

    assert login.status_code == 200

    token = login.json()["access_token"]

    # Attempt to delete department
    response = client.delete(
        f"/departments/{department_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"
