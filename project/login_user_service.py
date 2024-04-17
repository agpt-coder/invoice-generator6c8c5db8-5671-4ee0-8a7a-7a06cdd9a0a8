import datetime

import bcrypt
import jwt
import prisma
import prisma.models
from pydantic import BaseModel


class LoginUserOutput(BaseModel):
    """
    This model represents the response returned after successful user authentication, primarily consisting of the access token.
    """

    access_token: str
    token_type: str


async def login_user(email: str, password: str) -> LoginUserOutput:
    """
    Authenticates user and returns a token.

    This function attempts to authenticate a user using their email and password.
    If the authentication is successful, it generates and returns a JWT token encapsulated
    within a `LoginUserOutput` model. If authentication fails, it should raise an
    appropriate exception.

    Args:
        email (str): The email address of the user trying to log in.
        password (str): The password for the user trying to log in.

    Returns:
        LoginUserOutput: This model represents the response returned after successful user authentication, primarily consisting of the access token.

    Raises:
        ValueError: If the email does not exist in the database or the password doesn't match.

    Example:
        # Assuming the function is called within an async function or event loop
        result = await login_user('user@example.com', 'password123')
        print(result)
        > LoginUserOutput(access_token='eyJhb...', token_type='Bearer')
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user or not bcrypt.checkpw(
        password.encode("utf-8"), user.password.encode("utf-8")
    ):
        raise ValueError("Invalid email or password")
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }
    secret_key = "YourSecretKeyHere"
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return LoginUserOutput(access_token=token, token_type="Bearer")
