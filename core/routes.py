from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from core import schemas
from core.database import get_db
from sqlalchemy.orm import Session
from core.crud import (
    create_student_class, get_student_classes, get_student_class, update_student_class, delete_student_class,
    create_student, get_students, get_student, update_student, delete_student
)

router_websocket = APIRouter()
router_student_classes = APIRouter(prefix='/student_classes', tags=['student_class'])
router_students = APIRouter(prefix='/students', tags=['student'])


# WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def create_notification(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Пользователь #{user_id} вошёл в чат")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Ваше сообщение: {data}", websocket)
            await manager.broadcast(f"Сообщение от пользователя #{user_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Пользователь #{user_id} вышел из чата")


@router_student_classes.post("/", response_model=schemas.StudentClass)
async def create_student_class_route(category_data: schemas.StudentClassCreate, db: Session = Depends(get_db)):
    category = create_student_class(db, category_data)
    await create_notification(f"Добавлен новый класс: {category.name}")
    return category


@router_student_classes.get("/", response_model=List[schemas.StudentClass])
async def read_student_classes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = get_student_classes(db, skip=skip, limit=limit)
    return categories


@router_student_classes.get("/{student_class_id}", response_model=schemas.StudentClass)
async def read_student_class(student_class_id: int, db: Session = Depends(get_db)):
    category = get_student_class(db, student_class_id)
    return category


@router_student_classes.patch("/{student_class_id}", response_model=schemas.StudentClass)
async def update_student_class_route(student_class_id: int, student_class_data: schemas.StudentClassUpdate, db: Session = Depends(get_db)):
    updated_category = update_student_class(db, student_class_id, student_class_data)
    if updated_category:
        await create_notification(f"Обновлён класс студентов: {updated_category.name}")
        return updated_category
    return {"message": "Данный класс не найден"}


@router_student_classes.delete("/{student_class_id}")
async def delete_student_class_route(student_class_id: int, db: Session = Depends(get_db)):
    deleted = delete_student_class(db, student_class_id)
    if deleted:
        await create_notification(f"Удалён студенческий класс: ID {student_class_id}")
        return {"message": "Удалён студенческий класс"}
    return {"message": "Данный класс не найден"}


# Товары
@router_students.post("/", response_model=schemas.Student)
async def create_student_route(schema: schemas.StudentCreate, db: Session = Depends(get_db)):
    item = create_student(db, schema)
    await create_notification(f"Студент добавлен: {item.name}")
    return item


@router_students.get("/", response_model=List[schemas.Student])
async def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = get_students(db, skip=skip, limit=limit)
    return items


@router_students.get("/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    item = get_student(db, student_id)
    return item


@router_students.patch("/{student_id}")
async def update_student_route(student_id: int, schema: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated_item = update_student(db, student_id, schema)
    if updated_item:
        await create_notification(f"Студент обновлен: {updated_item.name}")
        return updated_item
    return {"message": "Данный студент не найден"}


@router_students.delete("/{item_id}")
async def delete_student_route(item_id: int, db: Session = Depends(get_db)):
    deleted = delete_student(db, item_id)
    if deleted:
        await create_notification(f"Студент удалён: номер {item_id}")
        return {"message": "Студент удалён"}
    return {"message": "Студент не найдет"}
