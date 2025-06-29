from pydantic import BaseModel
from datetime import datetime

class InvoiceBase(BaseModel):
    amount: float
    description: str | None = None
    client_name: str
    client_email: str | None = None
    
class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: int
    status: str
    created_at: datetime 
    updated_at: datetime 

    class Config:
        orm_mode = True  

class InvoiceUpdate(BaseModel):
    amount: float | None = None
    description: str | None = None
    client_name: str | None = None
    client_email: str | None = None
    status: str = "pending"  

    class Config:
        orm_mode = True  