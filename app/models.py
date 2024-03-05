from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, DateTime, text
from .database import base
from sqlalchemy.orm import relationship

class User(base):
    __tablename__ = "users"

    id = Column(type_=Integer, primary_key=True)
    full_name = Column(type_=Integer, nullable=True)
    username = Column(type_=String, nullable=False)
    password = Column(type_=String, nullable=False)
    timestamp = Column(type_=TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)


class Task(base):
    __tablename__ = "tasks"

    id = Column(type_=Integer, primary_key=True)
    title = Column(type_=String, nullable=False)
    detail = Column(type_=String, nullable=False)
    priority = Column(type_=String, nullable=False, server_default=text("medium"))
    timestamp = Column(type_=TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    owner_id = Column(ForeignKey("users.id", ondelete="CASCADE"), type_=Integer, nullable=False)
    owner = relationship("User")
