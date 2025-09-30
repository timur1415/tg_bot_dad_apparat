from database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    