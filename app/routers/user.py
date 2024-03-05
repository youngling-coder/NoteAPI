from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from typing import Optional
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{id}", response_model=schemas.ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found! Requested ID: {id}")

    return user


@router.post("/", response_model=schemas.ResponseUser, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/{id}", response_model=schemas.ResponseUser)
def update_user(id: int, updated_user: schemas.CreateUser, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    user_q = db.query(models.User).filter(models.User.id == id)
    user = user_q.first()

    if not user:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found! Requested ID: {id}")

    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update user! Requested ID: {id}")

    updated_user.password = utils.hash(updated_user.password)
    user_q.update(updated_user.model_dump(), synchronize_session=False)

    db.commit()

    return user_q.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    user_q = db.query(models.User).filter(models.User.id == id)

    user = user_q.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found! User ID: {id}")

    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete user! Requested ID: {id}")

    user_q.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
