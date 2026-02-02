from fastapi import APIRouter
from app.api import parameter_routes, material_routes, printer_routes, matching_routes, auth_routes

# 创建路由器实例
parameter_router = APIRouter()
material_router = APIRouter()
printer_router = APIRouter()
matching_router = APIRouter()
auth_router = APIRouter()

# 导入路由处理程序
from app.api import parameter_routes, material_routes, printer_routes, matching_routes, auth_routes