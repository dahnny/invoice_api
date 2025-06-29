from sqlalchemy import Column, Integer, String, TIMESTAMP,text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id",  ondelete="CASCADE"), nullable=False) 
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    status = Column(String, default='unpaid', nullable=False)  # e.g., unpaid, paid, overdue
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=text('now()'), nullable=False)
    
    owner = relationship("User")