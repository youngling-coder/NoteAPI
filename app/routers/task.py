from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import Optional, List
from ..import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id, models.Task.title.contains(search)).limit(limit=limit).offset(skip).all()

    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found")

    return tasks

@router.get("/{id}", response_model=schemas.Task)
def get_task(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found! ID: {id}")

    return task

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Task)
def create_task(task: schemas.CreateTask, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    new_task = models.Task(owner_id=current_user.id, **task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    task_q = db.query(models.Task).filter(models.Task.id == id)

    task = task_q.first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found! Task ID: {id}")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete task! Requested ID: {id}")

    task_q.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Task)
def update_task(id: int, updated_task: schemas.CreateTask, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    task_q = db.query(models.Task).filter(models.Task.id == id)
    task = task_q.first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found! Requested ID: {id}")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update task! Requested ID: {id}")

    task_q.update(updated_task.model_dump(), synchronize_session=False)

    db.commit()

    return task_q.first()
