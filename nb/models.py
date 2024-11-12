from enum import unique

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text,TypeDecorator
import json
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    fullName = Column(String(100), unique=False, nullable=True)
    email = Column(String(100), unique=False, nullable=True)
    accountStatus = Column(String(20), unique=False, nullable=True, default="active") #["active", "blocked", "timedOut"]
    accessToken = Column(String(200), unique=True, nullable=False)
    creationTime = Column(String(200), unique=False, nullable=True)
    password = Column(String(200), unique=False)