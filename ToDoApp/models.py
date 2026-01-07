from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base):

    # naming the table in the DB
    __tablename__ = "todos"

    #defining the various columns in the table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    