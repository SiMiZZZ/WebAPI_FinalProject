from sqlalchemy.orm import Session

import core.schemas as schemas
from models import Student, StudentClass


# StudentClass
def create_student_class(db: Session, schema: schemas.StudentClassCreate):
    db_student_class = StudentClass(**schema.model_dump())
    db.add(db_student_class)
    db.commit()
    db.refresh(db_student_class)
    return db_student_class


def get_student_classes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(StudentClass).offset(skip).limit(limit).all()


def get_student_class(db: Session, student_class_id: int):
    return db.query(StudentClass).filter_by(id=student_class_id).first()


def update_student_class(db: Session, student_class_id: int, student_class_data: schemas.StudentClassUpdate | dict):
    db_student_class = db.query(StudentClass).filter_by(id=student_class_id).first()

    student_class_data = student_class_data if isinstance(student_class_data, dict) else student_class_data.model_dump()

    if db_student_class:
        for key, value in student_class_data.items():
            if hasattr(db_student_class, key):
                setattr(db_student_class, key, value)

        db.commit()
        db.refresh(db_student_class)

    return db_student_class


def delete_student_class(db: Session, student_class_id: int):
    db_category = db.query(StudentClass).filter_by(id=student_class_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# Student
def create_student(db: Session, schema: schemas.StudentCreate):
    db_item = Student(**schema.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Student).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    return db.query(Student).filter_by(id=student_id).first()


def update_student(db: Session, student_id: int, student_data: schemas.StudentUpdate | dict):
    db_item = db.query(Student).filter_by(id=student_id).first()

    student_data = student_data if isinstance(student_data, dict) else student_data.model_dump()

    if db_item:
        for key, value in student_data.items():
            if hasattr(db_item, key):
                setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item
    return None


def delete_student(db: Session, student_id: int):
    db_item = db.query(Student).filter_by(id=student_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
