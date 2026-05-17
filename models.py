from sqlalchemy import Column, String, Integer
from database import Base

class Recipes(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    count_watch = Column(Integer)
    time_cooking = Column(Integer)
    ingredient = Column(String)
    description = Column(String)
