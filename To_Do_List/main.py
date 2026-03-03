from fastapi import FastAPI, Depends, HTTPException ,status
from fastapi.responses import HTMLResponse
from fastapi import Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import models, schemas, auth
from database import engine, get_db
from deps import get_current_user

app = FastAPI(debug=True)
models.Base.metadata.create_all(bind= engine)

templates = Jinja2Templates(directory="templates")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


## Register

@app.post("/register")
def register(user: schemas.UserCreate,db: Session= Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="email already registered"
        )
    hashed = auth.hash_password(user.password)
    new_user = models.User(
        email = user.email,
        hashed_password=hashed
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
    # Login → JWT Token
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db : Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()
    
    if not user or not auth.verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = auth.create_access_token(
        {"sub" : str(user.id)}
    )
    
    return {
    "access_token": token,
    "token_type": "bearer"
}
    
    
@app.post("/tasks")
def cerate_task(
    task:schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user : models.User = Depends(get_current_user)
):
    new_task = models.Task(
        title = task.title,
        description = task.description,
        owner_id = current_user.id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task


@app.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Task).filter(
        models.Task.owner_id == current_user.id
    ).all()



@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    updated_task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(404, "Task not found")

    task.title = updated_task.title
    task.description = updated_task.description

    db.commit()
    db.refresh(task)

    return task


  
    
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(404 , "task not found ")
    
    db.delete(task)
    db.commit()
    
    return {"massage" : "delete"}