from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship



class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    department = Column(String(100), nullable=False)  # Temporary: old column

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )
    department_info = relationship("Department", back_populates="employees")

    salary = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)



class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    employees = relationship("Employee", back_populates="department_info")





class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user", nullable=False)