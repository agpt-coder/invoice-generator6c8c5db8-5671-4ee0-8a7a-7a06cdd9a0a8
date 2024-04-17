from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileModel(BaseModel):
    """
    The structured data of a user's profile, including personal and billing information.
    """

    firstName: str
    lastName: str
    companyName: Optional[str] = None
    address: str
    taxId: Optional[str] = None


class UserProfileUpdateResponse(BaseModel):
    """
    The response model for the 'update_profile' endpoint, confirming the update was successful and providing the updated profile data.
    """

    success: bool
    message: str
    updatedProfile: Optional[UserProfileModel] = None


async def update_profile(
    firstName: Optional[str],
    lastName: Optional[str],
    companyName: Optional[str],
    address: Optional[str],
    taxId: Optional[str],
) -> UserProfileUpdateResponse:
    """
    Updates user's profile information.

    Args:
        firstName (Optional[str]): The user's first name.
        lastName (Optional[str]): The user's last name.
        companyName (Optional[str]): The name of the company the user is associated with.
        address (Optional[str]): The user's current address.
        taxId (Optional[str]): The tax identification number of the user or their company.

    Returns:
        UserProfileUpdateResponse: The response model for the 'update_profile' endpoint, confirming the update was successful and providing the updated profile data.
    """
    current_user_id = "put_the_current_user_id_here"
    user_profile = await prisma.models.UserProfile.prisma().find_unique(
        where={"userId": current_user_id}
    )
    if user_profile:
        update_data = {}
        if firstName is not None:
            update_data["firstName"] = firstName
        if lastName is not None:
            update_data["lastName"] = lastName
        if companyName is not None:
            update_data["companyName"] = companyName
        if address is not None:
            update_data["address"] = address
        if taxId is not None:
            update_data["taxId"] = taxId
        updated_user_profile = await prisma.models.UserProfile.prisma().update(
            where={"userId": current_user_id}, data=update_data
        )
        updated_profile_model = UserProfileModel(
            firstName=updated_user_profile.firstName,
            lastName=updated_user_profile.lastName,
            companyName=updated_user_profile.companyName,
            address=updated_user_profile.address,
            taxId=updated_user_profile.taxId,
        )
        return UserProfileUpdateResponse(
            success=True,
            message="Profile updated successfully",
            updatedProfile=updated_profile_model,
        )
    else:
        return UserProfileUpdateResponse(
            success=False, message="User profile not found"
        )
