from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.utils.auth import get_current_active_user
from app.models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 依赖项：获取当前活跃用户
get_current_active_user = get_current_active_user