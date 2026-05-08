from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Any

import models
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zooki App Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserSyncData(BaseModel):
    user_id: str
    user: dict
    tracking: List[dict]

@app.post("/api/sync")
def sync_data(data: UserSyncData, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == data.user_id).first()
    
    if not db_user:
        db_user = models.User(
            user_id=data.user_id,
            name=data.user.get("name"),
            phone=data.user.get("phone"),
            gender=data.user.get("gender"),
            age=data.user.get("age"),
            weight=data.user.get("weight"),
            height=data.user.get("height"),
            bmi=data.user.get("bmi"),
            goal=data.user.get("goal"),
            activity=data.user.get("activity"),
            created_at=data.user.get("createdAt"),
            tracking_data=data.tracking
        )
        db.add(db_user)
    else:
        # Update existing
        db_user.tracking_data = data.tracking
        
    db.commit()
    return {"status": "success"}

@app.get("/api/user/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "user_id": db_user.user_id,
        "user": {
            "name": db_user.name,
            "phone": db_user.phone,
            "gender": db_user.gender,
            "age": db_user.age,
            "weight": db_user.weight,
            "height": db_user.height,
            "bmi": db_user.bmi,
            "goal": db_user.goal,
            "activity": db_user.activity,
            "createdAt": db_user.created_at
        },
        "tracking": db_user.tracking_data
    }

@app.get("/api/admin/leads")
def get_leads(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    leads = []
    for u in users:
        leads.append({
            "user_id": u.user_id,
            "name": u.name,
            "phone": u.phone,
            "gender": u.gender,
            "age": u.age,
            "weight": u.weight,
            "height": u.height,
            "bmi": u.bmi,
            "goal": u.goal,
            "activity": u.activity,
            "registeredAt": u.created_at,
            "streak": calculate_streak(u.tracking_data)
        })
    return leads

def calculate_streak(tracking_data):
    if not tracking_data: return 0
    import datetime
    streak = 0
    today = datetime.datetime.now()
    dates = [t.get('date') for t in tracking_data if t.get('workout_done') or t.get('meals_done')]
    # simple mock streak calculation for admin
    return len(dates)
