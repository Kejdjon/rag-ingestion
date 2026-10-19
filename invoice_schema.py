from pydantic import BaseModel
from typing import Optional


class Invoice(BaseModel):
    invoice_number: Optional[str] = None
    customer: Optional[str] = None
    invoice_date: Optional[str] = None
    amount_due: Optional[str] = None
    services_provided: Optional[str] = None

    source_document: Optional[str] = None
    page_number: Optional[int] = None