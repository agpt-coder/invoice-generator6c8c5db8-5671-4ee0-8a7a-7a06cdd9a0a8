from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Confirms the successful registration of a new user, potentially returning an identifier or a token.
    """

    user_id: str
    message: str


async def register_user(
    email: str,
    password: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    company_name: Optional[str] = None,
    address: Optional[str] = None,
    tax_id: Optional[str] = None,
) -> UserRegistrationResponse:
    """
    Registers a new user.

    Args:
    email (str): Email address of the user. Must be unique.
    password (str): Password for the user account. Should meet security criteria.
    first_name (Optional[str]): First name of the user.
    last_name (Optional[str]): Last name of the user.
    company_name (Optional[str]): The name of the company the user represents or owns.
    address (Optional[str]): Physical address of the user or their company.
    tax_id (Optional[str]): Tax identification number of the user or their company.

    Returns:
    UserRegistrationResponse: Confirms the successful registration of a new user, potentially returning an identifier or a token.

    """
    try:
        new_user = await prisma.models.User.prisma().create(
            data={
                "email": email,
                "password": password,
                "UserProfile": {
                    "create": {
                        "firstName": first_name,
                        "lastName": last_name,
                        "companyName": company_name,
                        "address": address,
                        "taxId": tax_id,
                    }
                },
            }
        )
        return UserRegistrationResponse(
            user_id=new_user.id, message="User successfully registered."
        )
    except Exception as e:
        raise e
