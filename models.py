from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    gender = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    bmi = Column(Float)
    goal = Column(String)
    activity = Column(String)
    created_at = Column(String)
    
    # Store tracking as JSON
    tracking_data = Column(JSON, default=list)
