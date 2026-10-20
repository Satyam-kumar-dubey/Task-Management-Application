
from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel

def create_task(body: TaskSchema, db: Session ):
    data = body.model_dump()
    new_task = TaskModel(title = data["title"],
                         description = data["description"],
                         is_completed = data["is_completed"])
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    
    return {"Status": "Task Created Successfully","data": new_task }

def get_all_products(db : Session):
    data = db.query(TaskModel).all()
    
    return {"Status": "Success","data": data }
