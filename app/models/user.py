from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    max_tasks = Column(Integer, nullable=False)
    password = Column(String, nullable=False)

    tasks = relationship("Task", backref="worker", lazy="joined")
