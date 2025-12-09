from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, deps

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        owner_id=current_user.id,
        status="todo"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    status: Optional[str] = Query(None),
    owner_id: Optional[int] = Query(None)
):
    query = db.query(models.Task)

    if owner_id and current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Not authorized to view this task")
    
    if current_user.role == "manager":
        if owner_id:
            query = query.filter(models.Task.owner_id == owner_id)
    else:
        query = query.filter(models.Task.owner_id == current_user.id)

    if status:
        query = query.filter(models.Task.status == status)

    return query.all()

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if current_user.role != "manager" and task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
        
    if current_user.role != "manager":
        if task_update.status:
            task.status = task_update.status
    else:
        if task_update.title:
            task.title = task_update.title
        if task_update.description:
            task.description = task_update.description
        if task_update.status:
            task.status = task_update.status
        if task_update.score is not None:
            task.score = task_update.score
        if task_update.feedback:
            task.feedback = task_update.feedback
            
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_project_manager_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}