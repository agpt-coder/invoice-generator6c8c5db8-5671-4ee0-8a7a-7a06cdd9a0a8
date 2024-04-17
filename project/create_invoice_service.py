from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ServiceDetail(BaseModel):
    """
    Details of each service including billable hours and rate id.
    """

    serviceId: str
    hours: float
    rateId: str


class PartDetail(BaseModel):
    """
    Details of each part used including quantity and cost.
    """

    partId: str
    quantity: int
    cost: float


class CreateInvoiceOutput(BaseModel):
    """
    Output model for a newly created invoice, including all details for confirmation.
    """

    invoiceId: str
    status: str
    totalAmount: float


async def create_invoice(
    userId: str,
    services: List[ServiceDetail],
    parts: List[PartDetail],
    taxRateId: str,
    dueDate: str,
) -> CreateInvoiceOutput:
    """
    Creates a new invoice based on input parameters.

    Args:
        userId (str): The user ID of the invoice issuer.
        services (List[ServiceDetail]): List of services provided.
        parts (List[PartDetail]): List of parts used.
        taxRateId (str): Identifier for the applicable tax rate based on jurisdiction.
        dueDate (str): Due date for the invoice payment.

    Returns:
        CreateInvoiceOutput: Output model for a newly created invoice, including all details for confirmation.
    """
    due_date_parsed = datetime.strptime(dueDate, "%Y-%m-%d")
    invoice = await prisma.models.Invoice.prisma().create(
        data={
            "userId": userId,
            "dueDate": due_date_parsed,
            "status": prisma.enums.InvoiceStatus.DRAFT,
            "TaxRate": {"connect": {"id": taxRateId}},
            "BillableItems": {
                "create": [
                    *[
                        {
                            "serviceId": service.serviceId,
                            "rateId": service.rateId,
                            "hours": service.hours,
                        }
                        for service in services
                    ],
                    *[
                        {
                            "partId": part.partId,
                            "quantity": part.quantity,
                            "cost": part.cost,
                        }
                        for part in parts
                    ],
                ]
            },
        }
    )
    total_amount_placeholder = 0.0
    await prisma.models.Invoice.prisma().update(
        where={"id": invoice.id},
        data={
            "totalAmount": total_amount_placeholder,
            "status": prisma.enums.InvoiceStatus.SENT,
        },
    )
    return CreateInvoiceOutput(
        invoiceId=invoice.id,
        status=invoice.status,
        totalAmount=total_amount_placeholder,
    )
