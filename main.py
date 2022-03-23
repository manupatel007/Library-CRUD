from unicodedata import name
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

engine = create_engine("sqlite:///todooo.db")
Base = declarative_base()

# creating the database model for book
class Book(Base):
  __tablename__ = 'books'
  id = Column(Integer, primary_key=True)
  name = Column(String(50))
  author = Column(String(50))
  price = Column(Integer)

# db model for Score
class TypingScore(Base):
  __tablename__ = 'typingScore'
  id = Column(Integer, primary_key=True)
  name = Column(String(50))
  score = Column(Integer)



# creating the pydentic model
class Library(BaseModel):
  name:str
  author:str
  price:float

# for api update
class Library2(BaseModel):
  name:Optional[str] = None
  author:Optional[str] = None
  price:Optional[float] = None

# Pydantic model for scores
class Score(BaseModel):
  name:str
  score:int
  
# Initialize the database
Base.metadata.create_all(engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def getBooks():
  session = Session(bind=engine, expire_on_commit=False)
  book = session.query(Book).all()
  session.close()
  return book

@app.get("/book/{id}")
def getBookById(id:int):
  session = Session(bind=engine, expire_on_commit=False)
  book = session.query(Book).get(id)
  session.close()
  return book

@app.post("/create")
def postBooks(book:Library):
  # create a new database session
  session = Session(bind=engine, expire_on_commit=False)

  # create an instance of the ToDo database model
  book = Book(name = book.name, author = book.author, price = book.price)

  # add it to the session and commit it
  session.add(book)
  session.commit()

  # grab the id given to the object from the database
  id = book.id

  # close the session
  session.close()

  # return the id
  return f"created book with id {id}"

@app.put("/updateprice/{id}")
def updatePrice(id:int, price:float):
  session = Session(bind=engine, expire_on_commit=False)

  # get the todo item with the given id
  book = session.query(Book).get(id)

  # update todo item with the given task (if an item with the given id was found)
  if book:
      book.price = price
      session.commit()

  # close the session
  session.close()

  if not book:
      return {'success':False}

  return book

@app.put("/update/{id}")
def update(id:int, book:Library2):
  session = Session(bind=engine, expire_on_commit=False)

  # get the todo item with the given id
  book1 = session.query(Book).get(id)

  # update todo item with the given task (if an item with the given id was found)
  if book1:
      if(book.name):
        book1.name = book.name
      if(book.author):
        book1.author = book.author
      if(book.price):
        book1.price = book.price
      session.commit()

  # close the session
  session.close()

  if not book:
      return {'success':False}

  return book


@app.delete("/delete")
def deleteBooks(id:int):
  session = Session(bind=engine, expire_on_commit=False)

  book = session.query(Book).get(id)
  session.delete(book)
  session.commit()
  session.close()
  return {"success":True}

@app.get("/leaderboard")
def getLeaderboard():
  session = Session(bind=engine, expire_on_commit=False)
  scores = session.query(TypingScore).all()
  session.close()
  return scores

@app.post("/sendscore")
def sendScore(score:Score):
  session = Session(bind=engine, expire_on_commit=False)
  # checking if name already exists
  v = session.query(TypingScore).filter(TypingScore.name == score.name).first()
  if v:
    v.score = max(v.score, score.score)
  else:
    tscore = TypingScore(name=score.name, score=score.score)
    session.add(tscore)
  # saving score
  session.commit()
  session.close()
  return {"success":True}

@app.get("/namescore/{name}")
def getScoreByName(name:str):
  session = Session(bind=engine, expire_on_commit=False)
  v = session.query(TypingScore).filter(TypingScore.name == name).first()
  if v:
    return {"success":True,"data":v}
  else:
    return {"success":False}