from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base


class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    layer_height = Column(Float, nullable=False)  # 层高
    print_speed = Column(Integer, nullable=False)  # 打印速度
    infill_density = Column(Float, nullable=False)  # 填充密度
    print_temperature = Column(Integer, nullable=False)  # 打印温度
    bed_temperature = Column(Integer, nullable=False)  # 热床温度
    travel_speed = Column(Integer, nullable=False)  # 移动速度
    retraction_distance = Column(Float, nullable=False)  # 回抽距离
    retraction_speed = Column(Float, nullable=False)  # 回抽速度
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    materials = relationship("ParameterMaterial", back_populates="parameter")
    printers = relationship("ParameterPrinter", back_populates="parameter")


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)  # 材料名称
    brand = Column(String(100))  # 品牌
    filament_diameter = Column(Float, nullable=False)  # 耗材直径
    density = Column(Float)  # 密度
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    parameters = relationship("ParameterMaterial", back_populates="material")


class Printer(Base):
    __tablename__ = "printers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)  # 打印机名称
    manufacturer = Column(String(100))  # 制造商
    nozzle_diameter = Column(Float, nullable=False)  # 喷嘴直径
    max_print_temp = Column(Integer, nullable=False)  # 最大打印温度
    max_bed_temp = Column(Integer, nullable=False)  # 最大热床温度
    build_volume_x = Column(Integer, nullable=False)  # 构建体积X
    build_volume_y = Column(Integer, nullable=False)  # 构建体积Y
    build_volume_z = Column(Integer, nullable=False)  # 构建体积Z
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    parameters = relationship("ParameterPrinter", back_populates="printer")


class ParameterMaterial(Base):
    __tablename__ = "parameter_materials"
    
    id = Column(Integer, primary_key=True, index=True)
    parameter_id = Column(Integer, ForeignKey("parameters.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    
    # 关系
    parameter = relationship("Parameter", back_populates="materials")
    material = relationship("Material", back_populates="parameters")


class ParameterPrinter(Base):
    __tablename__ = "parameter_printers"
    
    id = Column(Integer, primary_key=True, index=True)
    parameter_id = Column(Integer, ForeignKey("parameters.id"), nullable=False)
    printer_id = Column(Integer, ForeignKey("printers.id"), nullable=False)
    
    # 关系
    parameter = relationship("Parameter", back_populates="printers")
    printer = relationship("Printer", back_populates="parameters")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FavoriteParameter(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parameter_id = Column(Integer, ForeignKey("parameters.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User")
    parameter = relationship("Parameter")


class MatchingHistory(Base):
    __tablename__ = "matching_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    printer_id = Column(Integer, ForeignKey("printers.id"))
    matched_parameters = Column(Text)  # 匹配到的参数ID列表
    score = Column(Float)  # 匹配分数
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User")
    material = relationship("Material")
    printer = relationship("Printer")