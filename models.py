from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class StudentClass(Base):
    __tablename__ = 'student_classes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
 #   items = relationship('Student', back_populates='studentclass')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    student_class_id = Column(Integer, ForeignKey('student_classes.id'))
  #  student_class = relationship('StudentClass', back_populates='students')
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())