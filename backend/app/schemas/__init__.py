from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# 参数相关模式
class ParameterBase(BaseModel):
    name: str
    layer_height: float
    print_speed: int
    infill_density: float
    print_temperature: int
    bed_temperature: int
    travel_speed: int
    retraction_distance: float
    retraction_speed: float
    description: Optional[str] = None


class ParameterCreate(ParameterBase):
    pass


class ParameterUpdate(BaseModel):
    name: Optional[str] = None
    layer_height: Optional[float] = None
    print_speed: Optional[int] = None
    infill_density: Optional[float] = None
    print_temperature: Optional[int] = None
    bed_temperature: Optional[int] = None
    travel_speed: Optional[int] = None
    retraction_distance: Optional[float] = None
    retraction_speed: Optional[float] = None
    description: Optional[str] = None


class Parameter(ParameterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 材料相关模式
class MaterialBase(BaseModel):
    name: str
    brand: Optional[str] = None
    filament_diameter: float
    density: Optional[float] = None
    description: Optional[str] = None


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    filament_diameter: Optional[float] = None
    density: Optional[float] = None
    description: Optional[str] = None


class Material(MaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 打印机相关模式
class PrinterBase(BaseModel):
    name: str
    manufacturer: Optional[str] = None
    nozzle_diameter: float
    max_print_temp: int
    max_bed_temp: int
    build_volume_x: int
    build_volume_y: int
    build_volume_z: int
    description: Optional[str] = None


class PrinterCreate(PrinterBase):
    pass


class PrinterUpdate(BaseModel):
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    nozzle_diameter: Optional[float] = None
    max_print_temp: Optional[int] = None
    max_bed_temp: Optional[int] = None
    build_volume_x: Optional[int] = None
    build_volume_y: Optional[int] = None
    build_volume_z: Optional[int] = None
    description: Optional[str] = None


class Printer(PrinterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 用户相关模式
class UserBase(BaseModel):
    username: str
    email: str
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 匹配结果模式
class MatchingRequest(BaseModel):
    material_id: Optional[int] = None
    printer_id: Optional[int] = None
    layer_height: Optional[float] = None
    infill_density: Optional[float] = None
    print_speed: Optional[int] = None


class MatchingResult(BaseModel):
    parameter: Parameter
    score: float
    reason: str


class MatchingResponse(BaseModel):
    results: List[MatchingResult]
    total_count: int