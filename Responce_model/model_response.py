
from datetime import datetime
from pydantic import BaseModel


class User_model(BaseModel):

    id : int

    username: str

    email: str

    created_at : datetime


class User_create(BaseModel):

    username : str

    email : str
               

class User_sort_date(BaseModel):

    username : str

    email : str

    created_at : datetime



class Config:
        orm_mode = True