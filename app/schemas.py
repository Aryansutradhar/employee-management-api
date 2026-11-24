
from pydantic import BaseModel, EmailStr, Field





class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    department_id: int = Field(gt=0)
    salary: float = Field(ge=0)
    is_active: bool = True


class EmployeeUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    department_id: int = Field(gt=0)
    salary: float = Field(ge=0)
    is_active: bool





class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = {"from_attributes": True}



class UserLogin(BaseModel):
    username: str
    password: str



from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    description: str = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class DepartmentUpdate(BaseModel):
    name: str
    description: str = None