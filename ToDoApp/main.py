from typing import Optional

from fastapi import FastAPI, status, HTTPException, Depends
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field


#declaring app
app = FastAPI()

# the below line is responsible for the creation of database in the backend
models.Base.metadata.create_all(bind=engine)


# get the database
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class ToDo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority between 1-5")
    complete: bool



@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.ToDos).all()


@app.get("/todo/{todo_id}")
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.ToDos)\
        .filter(models.ToDos.id == todo_id)\
        .first()  # '.first()' method returns the query in the first matching instance.
    if todo_model is not None:
        return todo_model
    else:
        raise http_exception()



# in order to create a model we have to use pydantic
@app.post("/todos/create")
async def add_todo(todo: ToDo, db: Session = Depends(get_db)):
    todo_model = models.ToDos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()
    return {
        'status': 201,
        'transaction': 'Successful'
    }


@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: ToDo, db: Session = Depends(get_db)):
    todo_model = db.query(models.ToDos)\
        .filter(models.ToDos.id == todo_id)\
        .first()
    if todo_model is None:
        raise http_exception()
    else:
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete

        db.add(todo_model)
        db.commit()
        return {
            'status': 200,
            'transaction': "Successful"
        }


@app.delete("/todo/{todo_id}")
async def delete(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.ToDos)\
        .filter(models.ToDos.id == todo_id)\
        .first()
    if todo_model is None:
        raise http_exception()

    db.query(models.ToDos).filter(models.ToDos.id == todo_id).delete()
    # todo_model.delete()
    db.commit()

    return success_response(200)


def success_response(success_code: int):
    return HTTPException(status_code=success_code, detail="Success")


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")