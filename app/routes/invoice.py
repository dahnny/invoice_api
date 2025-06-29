from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.pdf.generate import generate_invoice_pdf
from app.crud.invoice import *
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from app.models.user import User
from app.tasks.email import send_invoice_email
from app.core.config import settings
from typing import List


router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_new_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> InvoiceResponse:
    new_invoice = create_invoice(db, invoice, current_user.id)  
    if not new_invoice:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create invoice"
        )
    send_invoice_email.delay(
        new_invoice.client_email,
        { 
            "id": new_invoice.id,
            "client_email": new_invoice.client_email,
            "amount": new_invoice.amount,
            "description": new_invoice.description,
            "created_at": new_invoice.created_at.isoformat(),
        }
    )
    return new_invoice


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def read_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> InvoiceResponse:
    invoice = get_invoice(db, invoice_id)
    if not invoice or invoice.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    return invoice

@router.get("/", response_model=List[InvoiceResponse])
def read_invoices(
    _status: str = Query(None, description="Filter by invoice status"),
    client_email: str = Query(None, description="Filter by client email"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[InvoiceResponse]:
    invoices = get_invoices(db, current_user.id, status=_status, client_email=client_email)
    if not invoices:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No invoices found for this user"
        )
    return invoices


@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_new_invoice(
    invoice: InvoiceUpdate,
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> InvoiceResponse: 
    existing_invoice = get_invoice(db, invoice_id)
    if not existing_invoice or existing_invoice.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    updated_invoice = update_invoice(db, invoice_id, invoice)
    if not updated_invoice:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update invoice"
        )  
    return updated_invoice

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoices(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_invoice = get_invoice(db, invoice_id)
    if not existing_invoice or existing_invoice.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    if not delete_invoice(db, invoice_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete invoice"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{invoice_id}/pdf", response_class=Response)
def download_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = get_invoice(db, invoice_id)
    if not invoice or invoice.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Properly serialize the invoice data
    invoice_data = {
        'id': invoice.id,
        'owner_id': invoice.owner_id,
        'client_name': invoice.client_name,
        'client_email': invoice.client_email,
        'description': invoice.description,
        'amount': invoice.amount,
        'status': invoice.status,
        'created_at': invoice.created_at,  # Keep as datetime object
        'updated_at': invoice.updated_at
    }
    
    path = generate_invoice_pdf(invoice_data)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate PDF"
        )    
    with open(path, "rb") as f:
        return Response(
            content=f.read(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=invoice_{invoice.id}.pdf"
            }
        )
    


