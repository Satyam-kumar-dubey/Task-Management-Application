
from pydantic import BaseModel

class UserSchema(BaseModel):
    
    name : str
    username : str
    email : str
    password : str
    
class UserResponseSchema(BaseModel):
    
    name : str
    username : str
    email : str
    id : int