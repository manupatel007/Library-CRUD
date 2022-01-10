from fastapi import FastAPI, status, Response, Depends
from typing import Optional
from sqlalchemy.orm import Session
from models import engine, Book, Publisher
from schema import Library, Library2, PublisherHouse
from authentication import get_current_username

app = FastAPI()

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
def postBooks(response: Response, book:Library, username: str = Depends(get_current_username)):
  # create a new database session
  session = Session(bind=engine, expire_on_commit=False)

  # create an instance of the ToDo database model
  book = Book(name = book.name, author = book.author, price = book.price, isbnCode = book.isbnCode, publisher=book.publisher)

  try:
    # add it to the session and commit it
    session.add(book)
    session.commit()
  except:
      response.status_code = 404
      return {"success":False,"message":"isbncode is not unique"}

  # grab the id given to the object from the database
  id = book.id

  # close the session
  session.close()

  # return the id
  return f"created book with id {id}"

@app.put("/updateprice/{id}")
def updatePrice(id:int, price:float, username: str = Depends(get_current_username)):
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
def update(id:int, book:Library2, username: str = Depends(get_current_username)):
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

  return book1


@app.delete("/delete")
def deleteBooks(id:int, username: str = Depends(get_current_username)):
  session = Session(bind=engine, expire_on_commit=False)

  book = session.query(Book).get(id)
  session.delete(book)
  session.commit()
  session.close()
  return {"success":True, "book":book}


@app.post("/addPublisher")
def addPublisher(response: Response, publisher:PublisherHouse, username: str = Depends(get_current_username)):
  # create a new database session
  session = Session(bind=engine, expire_on_commit=False)

  # create an instance of the ToDo database model
  publisher1 = Publisher(name = publisher.name)
  session.add(publisher1)
  session.commit()

  # grab the id given to the object from the database
  id = publisher1.id

  # close the session
  session.close()

  # return the id
  return f"Added Publisher with id {id}"