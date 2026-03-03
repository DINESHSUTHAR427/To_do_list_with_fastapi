from pydantic import BaseModel , EmailStr, Field

class UserCreate(BaseModel):
    email : EmailStr
    password : str = Field(
        min_length=6,
        max_length=72
        
    )
    
class UserOut(BaseModel):
    id : int
    email : EmailStr
    
    class Config:
        from_attributes = True
        
class TaskCreate(BaseModel):
    title :str
    description: str
    
class TaskOu(BaseModel):
    id: int
    title: str
    description:str
    is_completed:bool
    
    class Config :
        from_attributes = True