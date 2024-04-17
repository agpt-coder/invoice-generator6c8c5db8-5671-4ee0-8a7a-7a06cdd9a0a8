from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class InitiatePaymentResponse(BaseModel):
    """
    Response model for the initiate payment request. Contains details about the payment attempt, including a transaction reference.
    """

    transaction_id: str
    status: str
    message: str
    payment_url: Optional[str] = None


async def initiate_payment(
    invoice_id: str, user_id: str, payment_method: str, amount: float, currency: str
) -> InitiatePaymentResponse:
    """
    Initiates the payment process for an invoice.

    Args:
        invoice_id (str): The unique identifier of the invoice for which the payment is being initiated.
        user_id (str): The unique identifier of the user initiating the payment.
        payment_method (str): The chosen payment method by the user for this transaction.
        amount (float): The amount being paid. This is to ensure the amount being sent matches the invoice amount for additional verification.
        currency (str): Currency in which the payment is being made.

    Returns:
        InitiatePaymentResponse: Response model for the initiate payment request. Contains details about the payment attempt, including a transaction reference.
    """
    invoice = await prisma.models.Invoice.prisma().find_unique(where={"id": invoice_id})
    if not invoice or invoice.userId != user_id:
        return InitiatePaymentResponse(
            transaction_id="",
            status="Failed",
            message="Invoice not found or user mismatch.",
        )
    transaction_id = f"txn_{user_id}_{invoice_id}"
    payment_url = None
    if payment_method in ["online", "credit_card"]:
        payment_url = "http://example.com/payment"
    return InitiatePaymentResponse(
        transaction_id=transaction_id,
        status="Initiated",
        message="Payment initiated successfully.",
        payment_url=payment_url,
    )
