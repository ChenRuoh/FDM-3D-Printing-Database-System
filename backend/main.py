from fastapi import FastAPI
from app.database import engine
from app.api import routers

app = FastAPI(
    title="FDM 3D打印工艺参数数据库与匹配系统",
    description="用于管理FDM 3D打印工艺参数的数据库和匹配系统",
    version="1.0.0"
)

# 创建数据库表
from app.models import Base
Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(routers.parameter_router, prefix="/api/parameters", tags=["parameters"])
app.include_router(routers.material_router, prefix="/api/materials", tags=["materials"])
app.include_router(routers.printer_router, prefix="/api/printers", tags=["printers"])
app.include_router(routers.matching_router, prefix="/api/matching", tags=["matching"])

@app.get("/")
def read_root():
    return {"message": "欢迎使用FDM 3D打印工艺参数数据库与匹配系统"}