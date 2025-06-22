from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate
from typing import List

def create_invoice(db: Session, invoice: InvoiceCreate, user_id: int) -> Invoice:
    db_invoice = Invoice(
        **invoice.dict(),
        owner_id=user_id
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoice(db: Session, invoice_id: int) -> Invoice | None:
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def get_invoices(db: Session, user_id: int, status: str | None, client_email: str | None) -> List[Invoice]:    
    filters = [Invoice.owner_id == user_id]

    if status:
        filters.append(Invoice.status == status)
    
    if client_email:
        filters.append(Invoice.client_email == client_email)

    return (
        db.query(Invoice)
        .filter(*filters)
        .order_by(Invoice.created_at.desc())
        .all()
    )

def update_invoice(db: Session, invoice_id: int, invoice: InvoiceUpdate) -> Invoice | None:
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return None
    
    for key, value in invoice.dict().items():
        setattr(db_invoice, key, value)
        
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def delete_invoice(db: Session, invoice_id: int) -> bool:
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        return False
    
    db.delete(db_invoice)
    db.commit()
    return True



