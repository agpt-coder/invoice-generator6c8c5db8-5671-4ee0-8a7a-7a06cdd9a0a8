from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class VerifyPaymentResponse(BaseModel):
    """
    The response provides details on the verified payment transaction, including its current status.
    """

    transactionId: str
    status: str
    errorMessage: Optional[str] = None


async def verify_payment(transactionId: str) -> VerifyPaymentResponse:
    """
    Verifies the status of a payment transaction.

    Args:
        transactionId (str): The unique identifier for the payment transaction to be verified.

    Returns:
        VerifyPaymentResponse: The response provides details on the verified payment transaction, including its current status.
    """
    payment_record = await prisma.models.Payment.prisma().find_unique(
        where={"transactionId": transactionId}, include={"Invoice": True}
    )
    if not payment_record:
        return VerifyPaymentResponse(
            transactionId=transactionId,
            status="Failed",
            errorMessage="Transaction not found.",
        )
    if payment_record.Invoice.status == prisma.enums.InvoiceStatus.PAID:
        status = "Completed"
    elif payment_record.Invoice.status in [
        prisma.enums.InvoiceStatus.DRAFT,
        prisma.enums.InvoiceStatus.SENT,
    ]:
        status = "Pending"
    else:
        status = "Failed"
        errorMessage = "Payment failed or cancelled."
        return VerifyPaymentResponse(
            transactionId=transactionId, status=status, errorMessage=errorMessage
        )
    return VerifyPaymentResponse(transactionId=transactionId, status=status)
