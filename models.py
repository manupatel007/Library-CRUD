from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///Advancedlibrary.db")
Base = declarative_base()

# creating the database model
class Publisher(Base):
  __tablename__ = 'publishers'
  id = Column(Integer, primary_key=True)
  name = Column(String(50))

# creating the database model
class Book(Base):
  __tablename__ = 'books'
  id = Column(Integer, primary_key=True)
  name = Column(String(50))
  author = Column(String(50))
  price = Column(Integer)
  isbnCode = Column(String(50), unique=True, nullable=False)
  publisher = Column(Integer, ForeignKey('publishers.id'))

Base.metadata.create_all(engine)