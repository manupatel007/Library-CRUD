from pydantic import BaseModel
from typing import Optional

# creating the pydentic model
class Library(BaseModel):
  name:str
  author:str
  price:float
  isbnCode:str
  publisher:int

# for api update
class Library2(BaseModel):
  name:Optional[str] = None
  author:Optional[str] = None
  price:Optional[float] = None
  isbnCode:Optional[str] = None
  publisher:Optional[int] = None

class PublisherHouse(BaseModel):
    name:str