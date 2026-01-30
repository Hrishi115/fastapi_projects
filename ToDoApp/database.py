from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()


SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

#making sure only one thread is not used for one transaction
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#making sure everything is under control and nothing is happening automatically
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()