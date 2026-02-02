from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 数据库URL - 使用SQLite
DATABASE_URL = "sqlite:///../database/db.sqlite"

# 创建引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础类
Base = declarative_base()