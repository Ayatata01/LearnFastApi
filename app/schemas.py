from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

    # --PYDANTIC MODEL OF POST SCHEMA--

# POST SCHEMA
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #default value of published is true 
    # rating: Optional[int] = None

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True 

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool

    # -- ENHERITENCE --
# class PostCreate(PostBase):
#     pass

    #  -- RESPONSE SCHEMA IT WILL SEND RESPONSE STRUCTURE EXACTLY LOOKS LIKE THIS CLASS WHEN YOU RETURN RESPONSE IN MAIN.PY--

#RESPONSE USER SCHEMA
class UserResponse(BaseModel):
    email : str
    id : str
    created_at : datetime

    class Config:
        orm_mode = True
        
class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    published : bool 
    created_at : datetime
    owner_id : int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


#USER CREATE SCHEMA
class UserBase(BaseModel):
    email : EmailStr
    password : str

class UserCreate(UserBase):
    pass


#USER AUTH lOGIN SHCHEMA
# class UserLogin(BaseModel):
#     email : EmailStr
#     password : str


#TOKEN SCHEMA
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None


# VOTE SCHEMA
class Vote(BaseModel):
    post_id: int 
    dir: conint(le= 1)



