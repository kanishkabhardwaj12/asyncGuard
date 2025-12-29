from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import enum
from sqlalchemy import Enum
from app.config.db import Base

class UserRole(enum.Enum):
    viewer = "viewer"
    auditor = "auditor"
    admin = "admin"


class User(Base):
    __tablename__= "users"
    
    id=Column(Integer, primary_key=True,unique=True)
    email=Column(String(255),unique=True,index=True,nullable=False)
    hashed_password=Column(String , nullable=False)
    role=Column(Enum(UserRole), nullable=False , default=UserRole.viewer)
    org_id=Column(Integer,ForeignKey("organizations.id",ondelete="SET NULL"),nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    organization = relationship("Organization", back_populates="users")