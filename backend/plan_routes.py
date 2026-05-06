from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

import models
import database
import ai_service

router = APIRouter()

class IdeaRequest(BaseModel):
    user_id: str
    idea: str

@router.post("/generate")
def generate_plan(request: IdeaRequest, db: Session = Depends(database.get_db)):
    plan_data = ai_service.generate_business_plan(request.idea)
    
    user_uuid = uuid.UUID(request.user_id)
    
    new_plan = models.BusinessPlan(
        user_id=user_uuid,
        title=plan_data.get("title", "New Plan"),
        idea_description=request.idea,
        plan_content=plan_data,
        status="complete"
    )
    
    db.add(new_plan)
    db.flush() # flush to get new_plan.id
    
    checklist_items = ai_service.generate_checklist(plan_data)
    new_checklist = models.Checklist(business_plan_id=new_plan.id)
    db.add(new_checklist)
    db.flush()
    
    for i, item in enumerate(checklist_items):
        ci = models.ChecklistItem(
            checklist_id=new_checklist.id,
            title=item.get("title", "Task"),
            description=item.get("description", ""),
            sort_order=i
        )
        db.add(ci)
        
    db.commit()
    db.refresh(new_plan)
    
    return {"plan_id": str(new_plan.id), "plan_content": plan_data, "checklist": checklist_items}

@router.get("/{plan_id}")
def get_plan(plan_id: str, db: Session = Depends(database.get_db)):
    plan = db.query(models.BusinessPlan).filter(models.BusinessPlan.id == uuid.UUID(plan_id)).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan
